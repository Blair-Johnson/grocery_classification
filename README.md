# Grocery Item Classification Model
Grocery classification model trained for Intel OpenVINO Summer Intern Challenge 2021
## About
This repository contains a MobileNetV3 image classifier trained on a combination of two open source grocery image datasets:
-  ```marcusklasson/GroceryStoreDataset```
-  ```abhinavsagar/Grocery-Product-Classification```  

The model is available in both TensorFlow ```saved_model``` format and OpenVINO Intermediate Representation under the ```models``` directory.
## Requirements
```
tensorflow==2.5.0
```
## Usage
### Inference
Just use the pretrained models along with the ```labels.csv``` mapping to classify grocery items in TensorFlow or OpenVINO.
The model expects and input size of ```(1, 224, 224, 3)``` and returns a softmax vector over the 60 classes included.
### Training
This training script is configured for GPU training. Some modifications may be required for CPU training.
If you wish to train from scratch or use your own model, see the following steps:

1. Clone the two datasets to the directory of your choosing:  
```
git clone https://github.com/abhinavsagar/Grocery-Product-Classification.git && git clone https://github.com/marcusklasson/GroceryStoreDataset.git
```
2. Ensure that you have TensorFlow and all of its dependencies installed:  
```
pip install -r requirements.txt
```
3. Modify ```train.py``` to replace MobileNetV3 with the model of your choice (if you so wish).  
4. Run ```train.py``` with the paths to both datasets specified:  
```
python3 train.py "${YOUR_PATH}/Grocery-Product-Classification" "${YOUR_PATH}/GroceryStoreDataset"
```  
5. Optional arguments are available to customize training hyperparameters. You can find these via:
```
python3 train.py -h
```

### Conversion
Run ```convert_savedmodel.py``` to convert the most recent training checkpoint to the TensorFlow ```saved_model``` format. As-is this will overwrite ```models/saved_models/MobileNetV3```. This can easily be changed via the script.
For instructions on converting the ```saved_model``` to OpenVINO, see the [OpenVINO Documentation](https://docs.openvinotoolkit.org/latest/openvino_docs_MO_DG_prepare_model_convert_model_Convert_Model_From_TensorFlow.html).

## Performance
The provided model has been trained for 61 epochs and acheived a top-1 validation accuracy of 72% on a random split of 600 validation images. The incorporated datasets are highly class-imbalanced, and accuracy will vary greatly by class.
The images are also taken from limited contexts, so performance may suffer in out-of-sample situations.

## Attribution
### Grocery Store Dataset
```
https://github.com/marcusklasson/GroceryStoreDataset

@inproceedings{klasson2019hierarchical,
  title={A Hierarchical Grocery Store Image Dataset with Visual and Semantic Labels},
  author={Klasson, Marcus and Zhang, Cheng and Kjellstr{\"o}m, Hedvig},
  booktitle={IEEE Winter Conference on Applications of Computer Vision (WACV)},
  year={2019}
}
```
### Grocery-Product-Classification
```
https://github.com/abhinavsagar/Grocery-Product-Classification
https://towardsdatascience.com/multi-class-object-classification-for-retail-products-aa4ecaaaa096

@misc{sagarmulti,
  Author = {Abhinav Sagar},
  Title = {Multi Class Object Classification for Retail Products},
  Year = {2019},
  Journal = {Towards Data Science},
}
```
