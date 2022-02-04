"""
   Resource     Method     Path          Parameters     Status

1. Register     POST       /register     username       200 OK
                                         password

2. Store        POST       /store        username       200 OK
                                         password       301 Out of Tokens
                                         sentence       302 Invalid Username/Password 

2. Retrieve     POST       /get          username       200 OK
                                         password       301 Out of Tokens
                                                        302 Invalid Username/Password                                         
"""

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase  # make a database
users = db["Users"]  # make a collection

class Register(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        hashed_pw = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())

        users.insert_one({
            "Username": username, 
            "Password": hashed_pw,
            "Sentence": "",
            "Tokens": 5
        })

        retJson = {
            "Status": 200,
            "Message body": "Successfully signed up for the API"
        }

        return jsonify(retJson)

def verifyPw(username, password):
    hashed_pw = users.find_one({
        "Username": username
    })["Password"]

    if bcrypt.hashpw(password.encode("utf8"), hashed_pw) == hashed_pw:
        return True
    else:
        return False

def countTokens(username, password):
    tokens = users.find_one({
        "Username": username
    })["Tokens"]

    return tokens

class Store(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]

        # verify username and password
        correct_pw = verifyPw(username, password)

        if not correct_pw:
            retJson = {
                "Status": 302
            }
            return jsonify(retJson)

        # veryfy enough tokens
        num_tokens = countTokens(username, password)

        if num_tokens <= 0:
            retJson = {
                "Status": 301
            }
            return jsonify(retJson)

        # store the sentence and take one token away
        users.update_one({
            "Username": username
        }, {
            "$set": {
                "Sentence": sentence,
                "Tokens": num_tokens-1
            }
        })

        retJson = {
            "Status": 200,
            "Message Body": "Sentence saved successfully"
        }

        return jsonify(retJson)

class Get(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        # verify username and password
        correct_pw = verifyPw(username, password)

        if not correct_pw:
            retJson = {
                "Status": 302
            }
            return jsonify(retJson)

        # veryfy enough tokens
        num_tokens = countTokens(username, password)

        if num_tokens <= 0:
            retJson = {
                "Status": 301
            }
            return jsonify(retJson)

        #make the user pay
        users.update_one({
            "Username": username
        }, {
            "$set": {
                "Tokens": num_tokens-1
            }
        })

        sentence = users.find_one({
            "Username": username
        })["Sentence"]

        tokens = users.find_one({
            "Username": username
        })["Tokens"]

        retJson = {
            "Status": 200,
            "Message Body": sentence,
            "Remaining Tokens": tokens
        }

        return jsonify(retJson)


api.add_resource(Register, "/register")
api.add_resource(Store, "/store")
api.add_resource(Get, "/get")

if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True)