from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class Add(Resource):
    def post(self):
        pass
    def get(self):
        pass
    def put(self):
        pass
    def delete(self):
        pass

class Subtract(Resource):
    pass

class Multiply(Resource):
    pass

class Divide(Resource):
    pass

@app.route('/')
def hello():
    return 'Hello World'

api.add_resource(Add, '/add')
api.add_resource(Subtract, '/sub')
api.add_resource(Multiply, '/mul')
api.add_resource(Divide, '/divide')

if __name__=="__main__":
    app.run(debug=True)