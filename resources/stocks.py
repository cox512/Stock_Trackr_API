import models
import random
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time
from dotenv import load_dotenv
load_dotenv()
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user

stock = Blueprint('stocks', 'stock') #Check out the Flask docs for more info on these two "stocks", "stock" uses.

@stock.route('/', methods=["GET"])
# @login_required
def get_all_stocks():
    print(current_user)
    try:
        #stocks = [model_to_dict(stock) for stock in current_user.stock]
        stocks = [model_to_dict(stock) for stock in models.Stock.select()]#Change the model class into a dictionary class, find all of the stock dicts (via 'select'). 
        # print(stocks)
        #Send those dicts back as a response.
        return jsonify(data=stocks, status={"code": 200, "message": "Success"})
    except models.DoesNotExist: #models.DoesNotExist is Flask specific error handling. It's thrown when the try does not work. It will throw a KeyError (which is the Python term).
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@stock.route('/', methods=['POST'])
# @login_required
def create_stocks(): #Peewee's create() method
    body = request.get_json() #'request' is a global object that is getting the json from our data request.
    print(type(body), 'body')
    new_stock = models.Stock.create(company_name=body['company_name'], ticker=body['ticker'], watchlist=body['watchlist']) #Spread, similar to the use of ... in javascript
    # print(new_stock.__dict__)
    # print(dir(new_stock))
    print(model_to_dict(new_stock), 'model to dict')
    stock_dict = model_to_dict(new_stock)
    return jsonify(data=stock_dict, status={'code': 201, 'message': "Success"})