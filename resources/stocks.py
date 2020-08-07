import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

stock = Blueprint('stocks', 'stock')

@stock.route('/', methods=["GET"])
def get_all_stocks():
    try:
        stocks = [model_to_dict(stock) for stock in models.Stock.select()]#Change the model class into a dictionary class, find all of the stock dicts (via 'select'). 
        print(stocks)
        #Send those dicts back as a response.
        return jsonify(data=stocks, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@stock.route('/', methods=['POST'])
def create_stocks(): #Peewee's create() method
    body = request.get_json() #'request' is a global object that is getting the json from our data request.
    # print(type(body), 'body')
    stock = models.Stock.create(**body) #Spread, similar to the use of ... in javascript
    print(stock.__dict__)
    print(dir(stock))
    print(model_to_dict(stock), 'model to dict')
    stock_dict = model_to_dict(stock)
    return jsonify(data=stock_dict, status={'code': 201, 'message': "Success"})