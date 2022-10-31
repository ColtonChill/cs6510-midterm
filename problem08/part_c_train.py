from tqdm import tqdm
from utils import *
import sys


data_path = os.path.join(os.getcwd(),"archive/agri_data/data")
files = os.listdir(data_path)
paths = sorted([os.path.join(data_path, os.path.splitext(s)[0]) for s in files if s.endswith('.txt')])

df = readLabels(paths) 

df.loc[(df.img_name == 'agri_0_3820'),'label']=1

# mean = 0.5, std = 0.5
transformer = transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]) 
avg_df = df.groupby('img_name',as_index=False).agg({
        'img_name':'first',
        'label':pd.Series.mode,
        'path':'first'})

train_df, test_df = train_test_split(avg_df, test_size=0.2)

train = PlantDataset(train_df,transform=transformer)
test = PlantDataset(test_df,transform=transformer)

trainloader = torch.utils.data.DataLoader(train, batch_size=16, shuffle=False, num_workers=2)
testloader = torch.utils.data.DataLoader(test, batch_size=16, shuffle=False, num_workers=2)

classes = ['crop', 'weed']

if len(sys.argv)<2:
    pretrain = True
elif sys.argv[1]=="pretrained":
    pretrain = True
elif sys.argv[1]=='untrained':
    pretrain = False
else:
    print(f'Error: Unknown option "{sys.argv[1]}", please use "pretrained" or "untrained".')
    sys.exit(0)

net = torchvision.models.alexnet(pretrained=pretrain)

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)


for epoch in range(2):  # loop over the dataset multiple times
    running_loss = 0.0
    with tqdm(trainloader, unit="batch") as tepoch:
        for name, imgs, labels in tepoch:
            # zero the parameter gradients
            optimizer.zero_grad()
            # forward + backward + optimize
            outputs = net(imgs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            # print statistics
            running_loss += loss.item()

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
    print(f'Epoch {epoch+1} Test:')
    for classname, correct_count in correct_pred.items():
        accuracy = 100 * float(correct_count) / total_pred[classname]
        print(f'\tAcc for class: {classname} is {accuracy:.2f} %')

    
torch.save(net.state_dict(), 'alexnet.pth')
print('Finished Training')