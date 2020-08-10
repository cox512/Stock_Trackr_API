import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user
from datetime import date

watchlist = Blueprint('watchlists', 'watchlist')

@watchlist.route('/', methods=['GET'])
@login_required
def get_all_watchlists():
    print(current_user.id)
    # print(current_user.watchlist)
    try:
        watchlists = [model_to_dict(watchlist) for watchlist in current_user.watchlist]
        # watchlists = [model_to_dict(watchlist) for watchlist in models.Watchlist.select()]
        
        return jsonify(data=watchlists, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@watchlist.route('/', methods=['POST'])
@login_required
def create_watchlists():
    print(request.get_json())
    body = request.get_json()
    # new_watchlist = models.Watchlist.create(**body)
    new_watchlist = models.Watchlist.create(title=body['title'], user=current_user.id, created_at=date.today())

    print(model_to_dict(new_watchlist))
    watchlist_dict = model_to_dict(new_watchlist)
    return jsonify(data=watchlist_dict, status={'code': 201, "messsage": "Success"})
