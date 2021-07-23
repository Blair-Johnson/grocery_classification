import os
import glob
import tensorflow as tf

if __name__ == '__main__':
    checkpoints = glob.glob('./models/checkpoints/*.hdf5')
    checkpoint_path = max(checkpoints, key = os.path.getctime)

    mNet = tf.keras.applications.MobileNetV3Small(input_shape = (224, 224, 3),
                        weights = None, include_top = False)
    model = tf.keras.models.Sequential([mNet,
                        tf.keras.layers.Flatten(),
                        tf.keras.layers.Dense(60, activation = 'softmax')])

    model.load_weights(checkpoint_path)
    model.save('./models/saved_models/MobileNetV3')
    print('done!')

