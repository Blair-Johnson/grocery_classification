import argparse
import datetime
import tensorflow as tf
from grocery.datasets import Combined
from grocery.transforms import simplify_labels, one_hot_labels, base_map, train_map, val_map

def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('GPC_path', help='Path to\
        Grocery-Product-Classification repository', type=str)
    parser.add_argument('GSD_path', help='Path to Grocery Store Dataset\
        repository', type=str)
    parser.add_argument('--start_lr', help='Starting learning rate',
        type=float, default = 1e-3)
    parser.add_argument('--val_samples', help='Number of validation samples',
        type=int, default = 600)
    parser.add_argument('--batch_size', help='Training batch size', type=int,
        default = 8)
    parser.add_argument('--early_stop', help='Epochs without progress before\
        early stop is triggered', type=int, default=15)
    parser.add_argument('--epochs', help='Maximum number of training epochs',
        type=int, default = 100)
    return parser.parse_args()

def init_dataset(path_label_mapping):
    paths = []
    labels = []
    for path, label in path_label_mapping.dataset.items():
        path, label = simplify_labels(path, label)
        paths.append(path)
        labels.append(label)
    
    labels, mapping = one_hot_labels(labels)
    print(mapping)
    return tf.data.Dataset.from_tensor_slices((paths,labels))


if __name__ == '__main__':
    args = init_args()

    path_maps = Combined(GPC_root_path = args.GPC_path, GSD_root_path =
                                                            args.GSD_path)
    dataset = init_dataset(path_maps)
    dataset = dataset.shuffle(10_000, reshuffle_each_iteration = False)
    dataset = dataset.map(base_map, num_parallel_calls = 6)
    val_set = dataset.take(args.val_samples)
    train_set = dataset.skip(args.val_samples)
    train_set = train_set.map(train_map, num_parallel_calls = 6)
    val_set = val_set.map(val_map, num_parallel_calls = 6)
    train_set = train_set.shuffle(buffer_size = 1000, seed = 10,
                        reshuffle_each_iteration = True)
    train_set = train_set.batch(args.batch_size)
    val_set = val_set.batch(args.batch_size)

    tf.config.list_physical_devices('GPU')
    config = tf.compat.v1.ConfigProto()
    config.gpu_options.allow_growth = True
    session = tf.compat.v1.Session(config = config)

    transfer_model = tf.keras.applications.MobileNetV3Small(input_shape = 
                        (224, 224, 3), include_top=False, weights='imagenet')
    model = tf.keras.models.Sequential([transfer_model, 
                                    tf.keras.layers.Flatten(),
                                    tf.keras.layers.Dense(60, activation = 
                                    'softmax')])
    model.compile(optimizer = tf.keras.optimizers.Adam(learning_rate = 
            args.start_lr),
            loss = 'categorical_crossentropy',
            metrics = ['accuracy'])

    log_dir = f'./logs/MobileNetV3-\
                    {datetime.datetime.now().strftime("%Y_%m_%d-%H_%M")}' 
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir = log_dir,
                    write_graph = True, update_freq = 4, profile_batch =
                    "100,200", histogram_freq = 1)
    checkpoint_path = f'./models/checkpoints/checkpoint-\
                    {datetime.datetime.now().strftime("%Y_%m_%d-%H_%M")}.hdf5'
    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,
                    verbose = 1, save_best_only = True, mode = 'min', monitor =
                    'val_loss', save_weights_only = True)
    plateau_callback = tf.keras.callbacks.ReduceLROnPlateau(verbose = 1, 
                    min_lr = 1e-5, factor = .1, patience = 10, cooldown = 3)
    earlystop_callback = tf.keras.callbacks.EarlyStopping(monitor = 'val_loss',
                    patience = args.early_stop, verbose = 1, mode = 'auto')
    callbacks = [tensorboard_callback, checkpoint_callback, plateau_callback,
                    earlystop_callback]
    
    model.fit(x = train_set,
              epochs = args.epochs,
              validation_data = val_set,
              callbacks = callbacks,
              verbose = 1,
              shuffle = True)

    print('done!')
