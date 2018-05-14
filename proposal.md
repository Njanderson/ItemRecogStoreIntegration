# CSE 455 Project Proposal

Nick Anderson | nja4

David Porter | davidpor

## Problem

In the UW CSE student stores (Snack Overflow for undergrads or the Benson store for grad students), some items do not have barcodes and must be input manually through selecting their picture in a menu or inputing their cost. The flow of scanning items is broken up by interacting with some UI.

## Solution

We propose a new feature for these stores - another camera that can be used to recognize and scan items by recognizing the object rather than requiring a barcode. For example, bananas need to be manually selected through a menu, whereas if we could recognize them with another camera, this will follow the barcode-oriented flow consumers are used to. We will train a model that can recognize some store items and "scan" them in real time, creating a store front UI that will demonstrate this functionality. Because there are already cameras in both stores, we do not expect that users will object to an item recognition camera being added. 

To do so, we want to use ImageNet's vast catalog of training image and perhaps collect some training images of our own. We want to train a PyTorch to perform this classification. 

Some stretch features would be to gather feedback from misclassifications to improve the model as more and more usage occurs.
