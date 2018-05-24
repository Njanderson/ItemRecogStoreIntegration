from flask import Flask, abort, request, jsonify
import json
from PIL import Image
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/infer', methods=["POST"])
def infer():
    data = request.get_data()
    #print(data)
    
    image = Image.open(BytesIO(base64.b64decode(data)))
    image.save("image.jpg", "JPEG")

    res = {"foo" : "bar"}
    response = jsonify(res)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
