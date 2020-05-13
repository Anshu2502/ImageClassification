from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import jwt
import datetime
from functools import wraps
import bcrypt
import logging
from pymongo import MongoClient
import json
import subprocess
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisthesecretkey'
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentenceDatabase
userReg = db["ImageClasify"]

class ClasifyImage(Resource):

    def post(self):
        data = request.get_json()
        url = data["url"]
        r = requests.get(url)
        retJson = {}
        if r.status_code == 200:
            with open("temp.jpg","wb") as f:
                f.write(r.content)
                process = subprocess.Popen('python classify_image.py --model_dir=. --image_file=./temp.jpg', shell=True)
                process.communicate()[0]
                process.wait()
                with open("text.txt") as g:
                    retJson = json.load(g)
        else:
            status = {"status ":"Error"}
            return status

        return retJson

api.add_resource(ClasifyImage, "/clasify")
@app.route('/')
def hello_world():
    return "Hello World!"


if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True)
