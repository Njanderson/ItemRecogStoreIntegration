import matplotlib.pyplot as plt
import numpy as np
import argparse

import torch
import torch.optim as optim


def log(str):
	print(str)


# def model_class(class_name):
#     return getattr(models, class_name)

# TODO Add more models if that is what we want to do
def argParser():
	parser = argparse.ArgumentParser(description='PyTorch Homework')
	parser.add_argument('--lr', default=0.01, type=float)
	parser.add_argument('--batchSize', default=4, type=int)
	parser.add_argument('--epochs', default=1, type=int)
	# parser.add_argument('--model', type=model_class)
	return parser.parse_args()
