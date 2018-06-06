import torch
import torchvision
import torchvision.transforms as transforms

class CifarLoader(object):
	"""Reference data loader"""
	def __init__(self, args):
		super(CifarLoader, self).__init__()
		transform = transforms.Compose(
			[
			 # TODO: Add data augmentations here
			 transforms.ToTensor(),
			 transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
			 ])

		transform_test = transforms.Compose([
			transforms.ToTensor(),
			transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)), 
		])

		#
		trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
												download=True, transform=transform)
		self.trainloader = torch.utils.data.DataLoader(trainset, batch_size=args.batchSize,
												  shuffle=True, num_workers=2)

		testset = torchvision.datasets.CIFAR10(root='./data', train=False,
											   download=True, transform=transform_test) 
		self.testloader = torch.utils.data.DataLoader(testset, batch_size=args.batchSize,
												 shuffle=False, num_workers=2)

		self.classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')


class ItemRecogLoader(object):
	"""ItemRecog data loader"""

	def __init__(self, args):
		super(ItemRecogLoader, self).__init__()
		# Found http://blog.outcome.io/pytorch-quick-start-classifying-an-image/
		# TODO: What does this *actually* do?
		normalize = transforms.Normalize(
			mean=[0.485, 0.456, 0.406],
			std=[0.229, 0.224, 0.225]
		)
		preprocess = transforms.Compose([
			transforms.Scale(256),
			transforms.CenterCrop(224),
			transforms.ToTensor(),
			normalize
		])

		# TODO: Switch to using this:
		# https://github.com/pytorch/examples/blob/master/imagenet/main.py

		img_pil = Image.open(io.BytesIO(response.content))

		trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
												download=True, transform=transform)
		self.trainloader = torch.utils.data.DataLoader(trainset, batch_size=args.batchSize,
													   shuffle=True, num_workers=2)

		testset = torchvision.datasets.CIFAR10(root='./data', train=False,
											   download=True, transform=transform_test)
		self.testloader = torch.utils.data.DataLoader(testset, batch_size=args.batchSize,
													  shuffle=False, num_workers=2)

		self.classes = ('banana', 'muffin')

