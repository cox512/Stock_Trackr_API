import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user

watchlist = Blueprint('watchlists', 'watchlist')

@watchlist.route('/', methods=['GET'])
def get_all_watchlists():
    try:
        watchlists = [model_to_dict(watchlist) for watchlist in models.Watchlist.select()]
        print(watchlists)
        return jsonify(data=watchlists, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@watchlist.route('/', methods=['POST'])
def create_watchlists():
    body = request.get_json()
    new_watchlist = models.Watchlist.create(**body)
    print(model_to_dict(watchlist))
    watchlist_dict = model_to_dict(new_watchlist)
    return jsonify(data=watchlist_dict, status={'code': 201, "messsage": "Success"})
