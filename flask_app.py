# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from route import route_service
from flask_cors import CORS

app = Flask(__name__)
# 使 jsonify 能够返回中文
app.config['JSON_AS_ASCII'] = False
CORS(app, supports_credentials=True)

@app.route('/route', methods=['GET'])
def route():
    params = request.json
    order_list = params["orders"]
    location = params["location"]
    return jsonify(route_service(order_list, location))

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
