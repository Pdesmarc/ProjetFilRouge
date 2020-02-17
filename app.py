from flask import Flask, request, jsonify
import os

#Init app
app = Flask(__name__)

@app.route('/', methods = ['GET'])
def get() : 
    return jsonify({'init': 'test flask server and postman'})

#Run server 
if  __name__=='__main__':
    app.run(debug=True)
