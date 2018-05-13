import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import os
import datetime
import pdb
import time
import torchvision.models as torchmodels

class BaseModel(nn.Module):
    def __init__(self):
        super(BaseModel, self).__init__()
        if not os.path.exists('logs'):
            os.makedirs('logs')
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S_log.txt')
        self.logFile = open('logs/' + st, 'w')

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
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        # TODO: Implement forward pass for CoolNet
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
