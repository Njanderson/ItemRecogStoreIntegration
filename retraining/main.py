import torch
from torch import nn
from torch import optim
from torch.utils.data import DataLoader
from torch.autograd import Variable

import torchvision
import pdb
import argparse
import os
import numpy as np

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data', dest="data_path", required=True, help="Path to data directory")
    parser.add_argument('-s', '--save', dest="save_path", required=True, help="Path of where to save to model")
    args = parser.parse_args()
    start_training(args.data_path, args.save_path)

def start_training(data_path, model_save_path):
    model = torchvision.models.vgg19(pretrained=True)

    # Disable modifying weights for earlier layers
    for param in model.parameters():
        param.requires_grad = False
        print(model)

        # Change the number of output features
        model.classifier[6].out_features = 3 # number of classes

        # Set requires_grad to True on the linear layer
        for param in model.classifier.parameters():
            param.requires_grad = True

        # Initialize the weights
        def weights_init(m):
            classname = m.__class__.__name__
            if classname.find('Linear') != -1:
                nn.init.kaiming_normal(m.weight.data)

        model.classifier.apply(weights_init)

        # Move the model to the GPU
        model = model.cuda()

        data_transforms = {
            'train':
            torchvision.transforms.Compose([
                torchvision.transforms.RandomSizedCrop(224),
                torchvision.transforms.RandomHorizontalFlip(),
                torchvision.transforms.ToTensor()
            ]),
            'test':
            torchvision.transforms.Compose([
                torchvision.transforms.Scale(256),
                torchvision.transforms.CenterCrop(224),
                torchvision.transforms.ToTensor()
            ])
        }

        image_dataset = {
            x: torchvision.datasets.ImageFolder(
                os.path.join(data_path, x), data_transforms[x])
            for x in ['train', 'test']
        }
        data_loader = {
            x: DataLoader(
                image_dataset[x], batch_size=4, shuffle=True, num_workers=1)
            for x in ['train', 'test']
        }

        class_names = image_dataset['train'].classes
        print("Classes : " + str(class_names))

        optimizer = optim.SGD(
            model.classifier.parameters(),
            lr=0.0001,
            momentum=0.9,
            nesterov=True,
            weight_decay=1e-6)
        criterion = nn.CrossEntropyLoss()

        epochs = 300
        dataset_sizes = {x: len(image_dataset[x]) for x in ['train', 'test']}

        # Train loop
        for epoch in range(epochs):
            print('Epoch {}/{}'.format(epoch, epochs - 1))

            for batch_i, data in enumerate(data_loader['train']):
                # pdb.set_trace()

                # get the inputs
                inputs, labels = data
                inputs = Variable(inputs.cuda())
                labels = Variable(labels.cuda())

                # zero the parameter gradients
                optimizer.zero_grad()

                # forward + backward + optimize
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                # print statistics
                if batch_i % 5 == 0:
                    print(
                        'epoch: {}, epoch progress: ({}/{} ({:.0f}%)) \tloss: {:.6f}'
                        .format(epoch, batch_i * len(data),
                                len(data_loader['train'].dataset),
                                100. * batch_i / len(data_loader['train']),
                                loss.data[0]))

            print("Saving...")
            save_checkpoint({
                'epoch': epoch,
                'state_dict': model.state_dict(),
                'optimizer': optimizer.state_dict(),
                'labels': class_names,
                'model': model
            }, model_save_path)
            test(
                model,
                data_loader['test'],
                classes=image_dataset['train'].classes)


def save_checkpoint(state, path):
    torch.save(state, path)
    pass

def test(net, dataloader, classes):
    # pdb.set_trace()
    correct = 0
    total = 0
    with torch.no_grad():
        for data in dataloader:
            images, labels = data
            images = images.cuda()
            labels = labels.cuda()

            outputs = net(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    print('Accuracy of the network: %d %%' % (100 * correct / total))

    class_correct = list(0. for i in range(len(classes)))
    class_total = list(0. for i in range(len(classes)))
    with torch.no_grad():
        for data in dataloader:
            images, labels = data

            images = images.cuda()
            labels = labels.cuda()

            outputs = net(images)
            _, predicted = torch.max(outputs, 1)
            c = (predicted == labels).squeeze()
            for i in range(len(labels)):
                label = labels[i]
                class_correct[label] += c[i].item()
                class_total[label] += 1

    for i in range(len(classes)):
        print('Accuracy of %5s : %2d %%' %
              (classes[i], 100 * class_correct[i] / class_total[i]))

if __name__ == '__main__':
    main()
