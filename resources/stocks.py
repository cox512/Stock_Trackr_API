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

#API search functions for stock
# lines = open('.env').read().splitlines()
# keys = random.choice(lines) #You can put multiple keys in the keys file. This way you can randomly choose between your keys and get more pulls.
# time = TimeSeries(key=keys, output_format='pandas')
# data, meta_data = time.get_intraday(symbol='MSFT', interval='5min', outputsize='full') #Look at docs for more options.
# # print(ticker)
# print(data)

# close_data = data['4. close']
# percent_change = close_data.pct_change() #pct_change() is a built in pandas function

# print(percent_change)

#Below is a sample that may help you create a stock alert later on.

# last_change = percent_change[-1]
# if abs(last_change) > 0.0004: #if absolute value of the last change is above 0.0004%, send an alert
#     print("AAPL Alert:" + last_change)

stock = Blueprint('stocks', 'stock') #Check out the Flask docs for more info on these two "stocks", "stock" uses.

@stock.route('/', methods=["GET"])
def get_all_stocks():
    try:
        stocks = [model_to_dict(stock) for stock in models.Stock.select()]#Change the model class into a dictionary class, find all of the stock dicts (via 'select'). 
        print(stocks)
        #Send those dicts back as a response.
        return jsonify(data=stocks, status={"code": 200, "message": "Success"})
    except models.DoesNotExist: #models.DoesNotExist is Flask specific error handling. It's thrown when the try does not work. It will throw a KeyError (which is the Python term).
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@stock.route('/', methods=['POST'])
def create_stocks(): #Peewee's create() method
    body = request.get_json() #'request' is a global object that is getting the json from our data request.
    # print(type(body), 'body')
    new_stock = models.Stock.create(**body) #Spread, similar to the use of ... in javascript
    # print(new_stock.__dict__)
    # print(dir(new_stock))
    print(model_to_dict(new_stock), 'model to dict')
    stock_dict = model_to_dict(new_stock)
    return jsonify(data=stock_dict, status={'code': 201, 'message': "Success"})