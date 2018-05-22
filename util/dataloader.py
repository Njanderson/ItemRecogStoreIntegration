import torch
import torchvision.datasets as datasets
import torchvision.transforms as transforms
import os

class ImageLoader(object):
	"""Loads images"""
	def __init__(self, traindir, valdir, batch_size):
		super(ImageLoader, self).__init__()
		# Taken from https://github.com/pytorch/examples/blob/master/imagenet/main.py
		normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
										 std=[0.229, 0.224, 0.225])

		# TODO: Can scan these in from the urls directory
		self.classes = ('muffin', 'banana')
		self.trainloader = torch.utils.data.DataLoader(
			datasets.ImageFolder(
				traindir,
				transforms.Compose([
					# transforms.RandomResizedCrop(224),
					# transforms.RandomHorizontalFlip(),
					# transforms.ToTensor(),
					# normalize,
					transforms.Resize((256, 256)),
					transforms.CenterCrop(224),
					transforms.ToTensor(),
					normalize,
				])
			),
			batch_size = batch_size
		)
		self.testloader = torch.utils.data.DataLoader(
			datasets.ImageFolder(
				valdir,
			 	transforms.Compose([
					transforms.Resize(256),
					transforms.CenterCrop(224),
					transforms.ToTensor(),
					normalize,
				])
			),
			batch_size = batch_size
		)
