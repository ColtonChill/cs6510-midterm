# Problem 8

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
Because of the size of the weight file, it could not be added to this repository. Therefore, you run the following code, please download [this file](https://drive.google.com/open?id=1-Aam2D-fqnwecbeHwa4rtzxtNjwcDkP6) from the above repository and place it in `YOLO_setup/data/weights/`.

Once the `crop_weed_detection.weights` file is downloaded, the demo code can be run:
```py
python part_b_demo.py
```
Be default, rendering of the YOLO boxes is turned on. Press `Q` to close the rendering window for each validation image.

## Part C
### Description:
Much like part A, the classifier here uses the same compressed labeling schema. Rather then using a normal CNN, this part uses a version of Alexnet provided by the pytorch framework. There are options on both `part_c_train.py` and `part_c_demo.py` to highlight the advantages of learning transfer. `part_c_train.py` has the options to pretrain the model with learning transfer (on by default). This can be toggled to highlight the training speed up that results from learning transfer. This option also exists for `part_c_demo.py`, however, it allows the user to toggle between a fine tuned model (generated with the above train code) vs. an only pretrained model. This helps shows that learning transfer is not enough to score well in a new domain.

### Instructions:
In order to run `part_c_demo.py`, you must either train a new alexnet model (`alexnet.pth`), or download a retrained model [here](https://drive.google.com/file/d/1MDoh_UsTUVMSJOI3n04t2-B-rYf5m3-r/view?usp=share_link), and place it in `problem08/`.

To train the model:
```py
python part_c_train.py <pretrained>|<untrained>
```
_*Note: The code will default to pretrained (learning transfer) if no option is given._

To demo the model:
```py
python part_c_train.py <retrained>|<untrained>
```
_*Note: The code will default to using a retrained model (using `alexnet.pth`) if no option is given._

## Part D
### Description:
Part D takes a large departure from the methodology of the previous 3 parts as this task requires the use of `Detectron2`. Detectron using a rather unique in-house framework build on pytorch with custom dataloader, model paradigms,  training regiments, and evaluation metrics. While quite the pain, this allows us to retrain and work on very powerful algorithms with minimal development overhead.

In this task, 3 models are implemented (Masked, Faster, RetinaNet R-CNN) and retrained to detect a new class of objects (party balloons in this case). Each model is then tested on the validation partition of the dataset.


### Instructions:
Because of the need for a GPU to run `Detectron2`, running code was implemented in Google Colab. The final `.ipynb` file is also included in this repo ([problem08_part_d.ipynb](problem08_part_d.ipynb)), however, the new object dataset and tested implementation is found there. Here is link to that drive should ([Google Colab](https://drive.google.com/drive/folders/1y1VXsz2n4byxgcOcAXxnSQ0V1X1rgsS9?usp=sharing)).


## References
* Dataloader: https://pytorch.org/tutorials/beginner/data_loading_tutorial.html
* Basic CNN: https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html
* YOLO Implementation: https://github.com/ravirajsinh45/Crop_and_weed_detection
* Detection2: https://detectron2.readthedocs.io/en/latest/index.html
