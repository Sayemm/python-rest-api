from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import spacy

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SimilarityDB
users = db["Users"]

def UserExist(username):
    if users.find({"Username":username}).count() == 0:
        return False
    else:
        return True
class Register(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        if UserExist(username):
            retJson = {
                "Status": 301,
                "Message Body": "Invalid Username Choose Another"
            }
            return jsonify(retJson)
        
        hashed_pw = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())

        users.insert_one({
            "Username": username,
            "Password": hashed_pw,
            "Tokens": 10
        })

        retJson = {
            "Status": 200,
            "Message Body": "Successfully signed up to the API"
        }

        return jsonify(retJson)

def verifyPw(username, password):
    if not UserExist(username):
        return False
    
    hashed_pw = users.find_one({
        "Username": username
    })["Password"]

    if bcrypt.hashpw(password.encode("utf"), hashed_pw) == hashed_pw:
        return True
    else:
        return False

def countTokens(username):
    tokens = users.find_one({
        "Username": username
    })["Tokens"]

    return tokens
class Detect(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        text1 = postedData["text1"]
        text2 = postedData["text2"]

        if not UserExist(username):
            retJson = {
                "Status": 301,
                "Message Body": "Invalid Username"
            }
            return jsonify(retJson)
        
        correct_pw = verifyPw(username, password)
        if not correct_pw:
            retJson = {
                "Status": 302,
                "Message Body": "Invalid Password"
            }
            return jsonify(retJson)

        num_tokens = countTokens(username)
        if num_tokens <= 0:
            retJson = {
                "Status": 303,
                "Message Body": "Out of tokens, please refill"
            }
            return jsonify(retJson)

        # calculate the edit distance
        nlp = spacy.load("en_core_web_sm")
        text1 = nlp(text1)
        text2 = nlp(text2)

        # ratio is between 0-1, closer to 1 means more similar
        ratio = text1.similarity(text2)

        retJson = {
            "Status": 200,
            "Similarity": ratio,
            "Message Body": "Similarity Score Calculated"
        }

        users.update_one({
            "Username": username
        }, {
           "$set": {
               "Tokens": num_tokens-1
           } 
        })

        return jsonify(retJson)