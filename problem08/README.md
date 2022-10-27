## Instructions:

To run the training code, you will need to download and unzip the data here in `problem08/` [Dataset](https://www.kaggle.com/datasets/ravirajsinh45/crop-and-weed-detection-data-with-bounding-boxes/download?datasetVersionNumber=1). This is so the dataloader can find the files. The demo code will work without the training data.

### Part A
```py
python part_a_demo.py
python part_a_train.py
```

Problems with a generic classification algo using YOLO data. YOLO boxes out objects and labels them individually, that is, there can be several labels per image. Luckily, this dataset doesn't have many mixed images, though there are some (`agri_0_3820`) 
