from flask import Flask, abort, request, jsonify
import json
from PIL import Image, ImageOps
from io import BytesIO
import base64
import random
import torch
import torchvision
import pdb

image_size = 224, 244

SAVE_MODEL_PATH="/tmp/store/model.pytorch" # TODO: make this an argument

app = Flask(__name__)

state = torch.load(SAVE_MODEL_PATH)

model = state['model'].cuda() # Move model to GPU
labels = state['labels']
model.eval() # Set the model to evaluation mode

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/infer', methods=["POST"])
def infer():
    data = request.get_data()
    #print(data)
    
    image = Image.open(BytesIO(base64.b64decode(data)))
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
    image_tensor = image_to_tensor(image).cuda()
    output = model(image_tensor)
    result_index = output.data.cpu().numpy().argmax()
    result = labels[result_index]
    return result

def image_to_tensor(pil_image):
    resized=ImageOps.fit(pil_image, image_size, Image.ANTIALIAS)
    loader = torchvision.transforms.Compose([
        torchvision.transforms.ToTensor()])
    return loader(resized).unsqueeze(0) 
