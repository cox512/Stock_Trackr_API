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
from resources.users import token_required


stock = Blueprint('stocks', 'stock') #Check out the Flask docs for more info on these two "stocks", "stock" uses.

@stock.route('/', methods=['POST'])
# @login_required
@token_required
def create_stocks(current_user): #Peewee's create() method
    body = request.get_json() #'request' is a global object that is getting the json from our data request.
    print("For Add Stock: ", body)
    new_stock = models.Stock.create(ticker=body["symbol"], watchlist=body["id"])
    # new_stock = models.Stock.create(ticker=body["ticker"], watchlist=body["watchlist"])

    print(model_to_dict(new_stock), 'model to dict')
    stock_dict = model_to_dict(new_stock)
    return jsonify(data=stock_dict, status={'code': 200, 'message': "Success"})

@stock.route('/showList', methods=["POST"])
# @login_required
@token_required
def get_all_stocks(current_user):
    print(current_user)
    try:
        body = request.get_json()
        print("watchlist ID: ", body)
        #stocks = [model_to_dict(stock) for stock in current_user.stock]
        # stocks = [model_to_dict(stock) for stock in models.Stock.select()]
        #Filter gets many items, 'get' just gets the first one.
        all_stocks = models.Stock.filter(watchlist=body["watchlist"])
        print(all_stocks)
        stocks = [model_to_dict(stock) for stock in all_stocks]
        #Change the model class into a dictionary class, find all of the stock dicts (via 'select'). 
        #Send those dicts back as a response.
        return jsonify(data=stocks, status={"code": 200, "message": "Success"})
    except models.DoesNotExist: #models.DoesNotExist is Flask specific error handling. It's thrown when the try does not work. It will throw a KeyError (which is the Python term).
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

#SHOW route
@stock.route('/<id>', methods=['GET'])
@token_required
# @login_required
def get_one_stock(current_user, id):
    print(id, 'stock id')
    stock = models.Stock.get_by_id(id)
    stock_dict = model_to_dict(stock)
    # print(stock_dict)
    return jsonify(data=stock_dict, status={"code": 200, "message": "Success"})

#UPDATE ROUTE
@stock.route('/<id>', methods=['PUT'])
# @login_required
@token_required
def update_stock(current_user, id):
    body = request.get_json()
    update_query = models.Stock.update(**body).where(models.Stock.id==id)
    #Always have to perform 'execute' on an update because of the method we're using with the database.
    update_query.execute()
    #After sending the query and executing it, we need 
    update_stock=models.Stock.get_by_id(id)
    return jsonify(data=model_to_dict(update_stock), status={"code": 200, "status": "Stock successfully updated."})

#DELETE ROUTE
@stock.route('/<id>', methods=['DELETE'])
@token_required
def delete_stock(current_user, id):
    print(id)
    print("models.Stock.id", models.Stock.get(models.Stock.id))
    stock_query = models.Stock.get(models.Stock.id==id).delete_instance()
    # print(models.Stock.get(models.Stock.watchlist))
    # stock_query.execute()
    return jsonify(data={}, success={"code": 200, "message": "Stock successfully deleted"})