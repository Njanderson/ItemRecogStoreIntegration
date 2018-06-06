from flask import Flask, abort, request, jsonify
import json
from PIL import Image, ImageOps
from io import BytesIO
import base64
import random
import torch
import torchvision
import pdb
import sys
import boto3
import uuid
import os
sys.path.append('..')
# from model.cnn import CoolNet

VGG = True
COOLNET = False


app = Flask(__name__)

if VGG:
    SAVE_MODEL_PATH = "model.pytorch"
    state = torch.load(SAVE_MODEL_PATH)
    model = state['model'] # Move model to GPU
    labels = state['labels']
    model.eval() # Set the model to evaluation mode
    image_size = 224, 244

if COOLNET:
    SAVE_MODEL_PATH="coolnet"
    model = CoolNet()
    model.load_state_dict(torch.load(SAVE_MODEL_PATH))
    labels = ('muffin', 'banana')
    model.eval() # Set the model to evaluation mode
    image_size = 256, 256

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/aws', methods=['POST'])
def aws():
    data = request.get_data()

    # Upload to S3
    s3client = boto3.client('s3', region_name='us-west-2')

    # Create bucket if not exists
    bucket_name = 'cse455-deepstore'
    
    # Use this to create the bucket if it doesn't exist...
    # s3client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'us-west-2'})

    # Upload image
    image_key = str(uuid.uuid4())

    # For use with Postman...
    s3client.put_object(Bucket=bucket_name, Key=image_key, Body=bytes(data))

    # If your webcam works...
    # s3client.put_object(Bucket=bucket_name, Key=image_key, Body=base64.b64decode(data))

    # Recognize the image
    rekogClient = boto3.client('rekognition')
    response = rekogClient.detect_labels(Image={'S3Object':{'Bucket':bucket_name,'Name':image_key}})
    
    # Server-side debugging
    print('Detected labels for ' + image_key)    
    for label in response['Labels']:
        print (label['Name'] + ' : ' + str(label['Confidence']))
    
    # Return labels and their confidence
    return "\n".join([label['Name'] + ' : ' + str(label['Confidence']) for label in response['Labels']])

@app.route('/infer', methods=["POST"])
def infer():
    data = request.get_data()
    #print(data)
    
    # image = Image.open(BytesIO(base64.b64decode(data)))
    image = Image.open(BytesIO(data))

    model_res = infer(model, labels, image)
    print("MODEL_RES output:", model_res)
    
    # generate a random price for fun :)
    price1 = str(random.randint(0, 9))
    price2 = str(random.randint(0, 9))
    price3 = str(random.randint(0, 9))
    finalPrice = price1 + "." + price2 + price3    

    res = {"name" : model_res, "price" : finalPrice}
    response = jsonify(res)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def infer(model, labels, image):
    image_tensor = image_to_tensor(image)
    # resize = torchvision.transforms.Resize(256, 256)
    output = model(image_tensor)
    print(output)
    result_index = output.data.cpu().numpy().argmax()
    result = labels[result_index]
    return result

def image_to_tensor(pil_image):
    resized = ImageOps.fit(pil_image, image_size, Image.ANTIALIAS)
    loader = torchvision.transforms.Compose([
        torchvision.transforms.ToTensor()])
    return loader(resized).unsqueeze(0) 

if __name__ == '__main__':
    app.run(port=3000)