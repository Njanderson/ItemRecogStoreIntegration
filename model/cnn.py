import matplotlib.pyplot as plt
import numpy as np
import torch
import os
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import datetime
import argparse
import time
import sys
sys.path.append('..')
from util.dataloader import ImageLoader

class BaseModel(nn.Module):
    def __init__(self):
        super(BaseModel, self).__init__()
        if not os.path.exists('logs'):
            os.makedirs('logs')
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H_%M_%S_log.txt')
        self.logFile = open(os.path.join('logs', st), 'w+')

    def log(self, str):
        print(str)
        self.logFile.write(str + '\n')

    def criterion(self):
        return nn.CrossEntropyLoss()

    def optimizer(self):
        return optim.SGD(self.parameters(), lr=0.001)

    def adjust_learning_rate(self, optimizer, epoch, args):
        lr = args.lr  # TODO: Implement decreasing learning rate's rules
        for param_group in optimizer.param_groups:
            param_group['lr'] = lr


class CoolNet(BaseModel):
    def __init__(self):
        super(CoolNet, self).__init__()
        # TODO: Define model here
        # self.conv1 = nn.Conv2d(3, 6, 5)
        # self.pool = nn.MaxPool2d(2, 2)
        # self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(3*224*224, 1024)
        self.fc2 = nn.Linear(1024, 256)
        self.fc3 = nn.Linear(256, 2)

    def forward(self, x):
        # TODO: Implement forward pass for CoolNet
        # x = self.pool(F.relu(self.conv1(x)))
        # x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 3*224*224)
        # x = x.view(-1, 150528)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x



def train(net, dataloader, optimizer, criterion, epoch):
    running_loss = 0.0
    total_loss = 0.0

    for i, data in enumerate(dataloader.trainloader, 0):
        # get the inputs
        inputs, labels = data

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
        if (i + 1) % 2000 == 0:    # print every 2000 mini-batches
            net.log('[%d, %5d] loss: %.3f' %
                  (epoch + 1, i + 1, running_loss / 2000))
            total_loss += running_loss
            running_loss = 0.0

    net.log('Final Summary:   loss: %.3f' %
          (total_loss / i))

def test(net, dataloader, tag=''):
    correct = 0
    total = 0
    if tag == 'Train':
        dataTestLoader = dataloader.trainloader
    else:
        dataTestLoader = dataloader.testloader
    with torch.no_grad():
        for data in dataTestLoader:
            images, labels = data
            outputs = net(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    net.log('%s Accuracy of the network: %d %%' % (tag,
        100 * correct / total))

    class_correct = list(0. for i in range(10))
    class_total = list(0. for i in range(10))
    with torch.no_grad():
        for data in dataTestLoader:
            images, labels = data
            outputs = net(images)
            _, predicted = torch.max(outputs, 1)
            c = (predicted == labels).squeeze()
            for i in range(4):
                label = labels[i]
                class_correct[label] += c[i].item()
                class_total[label] += 1


    for i in range(10):
        net.log('%s Accuracy of %5s : %2d %%' % (
            tag, dataloader.classes[i], 100 * class_correct[i] / class_total[i]))

def model_class(class_name):
    return getattr(class_name)


def argParser():
	parser = argparse.ArgumentParser(description='PyTorch Homework')
	parser.add_argument('--lr', default=0.01, type=float)
	parser.add_argument('--batchSize', default=4, type=int)
	parser.add_argument('--epochs', default=1, type=int)
	parser.add_argument('--model', type=model_class)
	return parser.parse_args()


def run_model():

    args = argParser()

    cifarLoader = ImageLoader(args)
    net = args.model()
    print('The log is recorded in ')
    print(net.logFile.name)

    criterion = net.criterion()
    optimizer = net.optimizer()

    for epoch in range(args.epochs):  # loop over the dataset multiple times
        net.adjust_learning_rate(optimizer, epoch, args)
        train(net, cifarLoader, optimizer, criterion, epoch)
        if epoch % 1 == 0: # Comment out this part if you want a faster training
            test(net, cifarLoader, 'Train')
            test(net, cifarLoader, 'Test')


    print('The log is recorded in ')
    print(net.logFile.name)

