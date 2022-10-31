from utils import *
import sys


data_path = os.path.join(os.getcwd(),"validation_imgs")
files = os.listdir(data_path)
paths = sorted([os.path.join(data_path, os.path.splitext(s)[0]) for s in files if s.endswith('.txt')])

df = readLabels(paths)
df = df.groupby('img_name',as_index=False).agg({
        'img_name':'first',
        'label':pd.Series.mode,
        'path':'first'})

# mean = 0.5, std = 0.5
transformer = transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]) 

test = PlantDataset(df,transform=transformer)

testloader = torch.utils.data.DataLoader(test, batch_size=16, shuffle=False, num_workers=2)

classes = ['crop', 'weed']

net = torchvision.models.alexnet(pretrained=True)
if len(sys.argv)<2:
    load_model = True
elif sys.argv[1]=="retrained":
    load_model = True
elif sys.argv[1]=='untrained':
    load_model = False
else:
    print(f'Error: Unknown option "{sys.argv[1]}", please use "retrained" or "untrained".')
    sys.exit(0)

if load_model: net.load_state_dict(torch.load('alexnet.pth'))

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

# prepare to count predictions for each class
correct_pred = {classname: 0 for classname in classes}
total_pred = {classname: 0 for classname in classes}

# again no gradients needed
with torch.no_grad():
    for i, (name, imgs, labels) in enumerate(testloader):
        outputs = net(imgs)
        _, predictions = torch.max(outputs, 1)
        # collect the correct predictions for each class
        for label, prediction in zip(labels, predictions):
            if label == prediction:
                correct_pred[classes[label]] += 1
            total_pred[classes[label]] += 1


# print accuracy for each class
print(f'Test:')
for classname, correct_count in correct_pred.items():
    accuracy = 100 * float(correct_count) / total_pred[classname]
    print(f'\tAcc for class: {classname} is {accuracy:.2f} %')