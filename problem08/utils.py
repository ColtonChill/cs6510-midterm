# from __future__ import print_function, division
import pandas as pd
import matplotlib.pyplot as plt # for plotting
import numpy as np # for transformation
import torch # PyTorch package
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision # load datasets

import torchvision.transforms as transforms 
from sklearn.model_selection import train_test_split
import cv2
import os


# Ignore warnings
import warnings
warnings.filterwarnings("ignore")


def show_img(path, labels=[]):
    fig = plt.figure()
    img = cv2.imread(path)
    width = img.shape[1]
    height = img.shape[0]
    for label in labels:
        x1 = int(np.around((label[0] - label[2]/2.0) * width))
        y1 = int(np.around((label[1] - label[3]/2.0) * height))
        x2 = int(np.around((label[0] + label[2]/2.0) * width))
        y2 = int(np.around((label[1] + label[3]/2.0) * height))
        plt.plot([x1,x2,x2,x1,x1],[y1,y1,y2,y2,y1], color='r')
        print(label[4])

    plt.imshow(img)
    plt.pause(30)
    plt.show()


def readLabels(paths):
    data = []
    for path in paths:
        with open(path+'.txt') as f:
            for line in f.readlines():
                d = [float(s) for s in line.strip().split(' ')]
                # move label to the back, add cat img_name & image_path 
                d = d[1:]+[int(d[0]), os.path.split(path)[1], path+'.jpeg']
                data.append(d)
    df = pd.DataFrame(data=data, columns=['x','y','width','height','label','img_name','path'])
    return df



class PlantDataset(torch.utils.data.Dataset):
    def __init__(self, df, transform=None):
        self.df = df
        self.transform = transform

    def __len__(self):
        return self.df.shape[0]

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        name,label,path = self.df.iloc[idx].to_numpy()
        img = cv2.imread(path)

        if self.transform:
            img = self.transform(img)

        return name,img,label

class NN(nn.Module):
    def __init__(self, input_size, output_size):
        super(NN, self).__init__()
	    # 3 input image channel, 6 output channels, 
	    # 5x5 square convolution kernel
        width, height = input_size[:2]
        self.conv1 = nn.Conv2d(input_size[2], 6, 5, stride=2)
	    # Max pooling over a (2, 2) window
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5, stride=2) 
        self.fc1 = nn.Linear(16 * 31*31, 120)# 5x5 from image dimension
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, output_size)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1) # flatten all dimensions except batch
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

"""
4: 3 x 512 x 512
4: 16 x 125 x 125
4: 250000
"""