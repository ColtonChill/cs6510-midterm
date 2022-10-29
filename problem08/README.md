## Part A

### Description:
This classifier is generic CNN saved in `generic_net.pth`. There are some problems with using a generic classification algo using YOLO data. YOLO boxes out objects and labels them individually, that is, there can be several labels per image where a generic CNN only outputs one label. Luckily, this dataset doesn't have many mixed images, though there are some (`agri_0_3820`). Therefore, we can take the mode of the YOLO labels and use that as the target for the generic CNN. 


### Instructions:
To run the training code, you will need to download and unzip the data here in `problem08/` ([Dataset](https://www.kaggle.com/datasets/ravirajsinh45/crop-and-weed-detection-data-with-bounding-boxes/download?datasetVersionNumber=1)). This is so the dataloader can find the files. The demo code will work without the training data.

To just run the demo code:
```py
python part_a_demo.py
```
To train the CNN on the above downloaded data:
```py
python part_a_train.py
```

## Part B
### Description:
This YOLO classifier is based off the implementation provided in the assignment description ([GitHub](https://github.com/ravirajsinh45/Crop_and_weed_detection)). This program uses the weights provided at this github repository, and doesn't implement retraining.


### Instructions:
Because of the size of the weight file, it could not be added to this repository. Therefore, you run the following code, please down load [this file](https://drive.google.com/open?id=1-Aam2D-fqnwecbeHwa4rtzxtNjwcDkP6) from the above repository and place it in `YOLO_setup/data/weights/`.

Once the `crop_weed_detection.weights` file is downloaded, the demo code can be run:
```py
python part_b_demo.py
```
Be default, rendering of the YOLO boxes is turned on. Press `Q` to close the rendering window for each validation image.

## Part C
### Instructions:
### Description:

## Part D
### Instructions:
### Description:


## References
* Dataloader: https://pytorch.org/tutorials/beginner/data_loading_tutorial.html
* Basic CNN: https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html
* YOLO Implementation: https://github.com/ravirajsinh45/Crop_and_weed_detection
