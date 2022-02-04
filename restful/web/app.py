from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

# same as docker-compose file db
# now client is connected to database
client = MongoClient("mongodb://db:27017")
db = client.aNewDB  # make a database
UserNum = db["UserNum"]  # make a collection

UserNum.insert_one({
    'num_of_users': 0
})

class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]['num_of_users']  # only has one document
        new_num = prev_num + 1

        db.UserNum.update_one({}, {'$set': {"num_of_users": new_num}})

        return str("Hello User " + str(new_num))

def checkPostedData(postedData, functionName):
    if functionName == 'add' or functionName == 'subtract' or functionName =='multiply':
        if "x" not in postedData or 'y' not in postedData:
            return 301
        else:
            return 200
    elif functionName == 'divide':
        if 'x' not in postedData or 'y' not in postedData:
            return 301
        elif int(postedData['y']) == 0:
            return 302
        else:
            return 200

class Add(Resource):
    def post(self):
        postedData = request.get_json()

        statusCode = checkPostedData(postedData, 'add')

        if statusCode != 200:
            retJson = {
                'Message': 'An error occurred',
                'Status Code': statusCode
            }

            return jsonify(retJson)

        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        retJson = {
            "Message": x + y,
            "Status Code": 200
        }
        return jsonify(retJson)

class Subtract(Resource):
    def post(self):
        postedData = request.get_json()

        statusCode = checkPostedData(postedData, 'subtract')

        if statusCode != 200:
            retJson = {
                'Message': 'An error occurred',
                'Status Code': statusCode
            }

            return jsonify(retJson)

        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        retJson = {
            "Message": x - y,
            "Status Code": 200
        }
        return jsonify(retJson)

class Multiply(Resource):
    def post(self):
        postedData = request.get_json()

        statusCode = checkPostedData(postedData, 'multiply')

        if statusCode != 200:
            retJson = {
                'Message': 'An error occurred',
                'Status Code': statusCode
            }

            return jsonify(retJson)

        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        retJson = {
            "Message": x * y,
            "Status Code": 200
        }
        return jsonify(retJson)

class Divide(Resource):
    def post(self):
        postedData = request.get_json()

        statusCode = checkPostedData(postedData, 'divide')

        if statusCode != 200:
            retJson = {
                'Message': 'An error occurred',
                'Status Code': statusCode
            }

            return jsonify(retJson)

        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        retJson = {
            "Message": (x*1.0) / y,
            "Status Code": 200
        }
        return jsonify(retJson)

@app.route('/')
def hello():
    return 'Hello World'

api.add_resource(Add, '/add')
api.add_resource(Subtract, '/subtract')
api.add_resource(Multiply, '/multiply')
api.add_resource(Divide, '/divide')
api.add_resource(Visit, "/hello")

if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True)