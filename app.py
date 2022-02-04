from crypt import methods
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "hello world"

@app.route('/hi')
def hi():
    return "hi"

@app.route('/bye')
def bye():
    retJson = {
        'field1': 'abc',
        'field2': 'def'
    }
    return jsonify(retJson)

@app.route('/add', methods=['POST'])
def add():
    dataDict = request.get_json()

    if 'y' not in dataDict: 
        return 'ERROR-x not found', 305

    x = dataDict['x']
    y = dataDict['y']
    z = x+y

    retJSON = {
        'z': z
    }
    return jsonify(retJSON), 200

@app.route('/sayem')
def sayem():
    age = 2*34
    retJson = {
        'number': age,
        'this is the name of my field': 'abc',
        'string': 'cde',
        'boolean': True,
        'null': None,
        'array': [1, 3, 5, "abcd"],
        'array of objects': [
            {
                'f1': 1
            },
            {
                'f2': "abcd"
            }
        ],
        'type': [
            {
                'mobile': [
                    {
                        'company': 'nokia',
                        'number': 45454
                    },
                    {
                        'company': 'sony',
                        'number': 1234
                    }
                ]
            }
        ]
    }

    return jsonify(retJson)

if __name__=="__main__":
    app.run(debug=True)