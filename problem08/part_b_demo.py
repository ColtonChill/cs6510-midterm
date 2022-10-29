from tqdm import tqdm
from utils import *
from YOLO_setup.darknet import *
from YOLO_setup.darknet_utils import *


data_path = os.path.join(os.getcwd(),"validation_imgs")
files = os.listdir(data_path)
paths = sorted([os.path.join(data_path, os.path.splitext(s)[0]) for s in files if s.endswith('.txt')])

df = readLabels(paths) 

# mean = 0.5, std = 0.5
transformer = transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]) 
df = df.groupby('img_name',as_index=False).agg({
        'img_name':'first',
        'label':pd.Series.mode,
        'path':'first'})

test = PlantDataset(df)

testloader = torch.utils.data.DataLoader(test, batch_size=1, shuffle=False, num_workers=1)

classes = ['crop', 'weed']

net = Darknet('YOLO_setup/data/cfg/crop_weed.cfg')
net.load_weights('YOLO_setup/data/weights/crop_weed_detection.weights')

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)


# prepare to count predictions for each class
correct_pred = {classname: 0 for classname in classes}
total_pred = {classname: 0 for classname in classes}

# again no gradients needed
with torch.no_grad():
    for i, (name, imgs, labels) in enumerate(testloader):
        original_image = cv2.cvtColor(imgs[0].reshape((512,512,3)).numpy(), cv2.COLOR_BGR2RGB)
        resized_image = cv2.resize(original_image, (net.width, net.height))
        predictions = detect_objects(net, resized_image, 0.4, 0.6)
        plot_boxes(original_image, predictions, classes, plot_labels = True)
        for label, prediction in zip(labels, [predictions[0][-1]]):
            if label == prediction:
                correct_pred[classes[label]] += 1
            total_pred[classes[label]] += 1


# print accuracy for each class
print(f'Test:')
for classname, correct_count in correct_pred.items():
    accuracy = 100 * float(correct_count) / total_pred[classname]
    print(f'\tAcc for class: {classname} is {accuracy:.2f} %')

####################