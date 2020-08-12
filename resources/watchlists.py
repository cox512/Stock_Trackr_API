import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user
from datetime import date

watchlist = Blueprint('watchlists', 'watchlist')

#SHOW route
@watchlist.route('/<id>', methods=['GET'])
def get_one_watchlist(id):
    print(id, 'watchlist id')
    watchlist = models.Watchlist.get_by_id(id)
    watchlist_dict = model_to_dict(watchlist)
    print(watchlist_dict)
    return jsonify(data=watchlist_dict, status={"code": 200, "message": "Success"})


@watchlist.route('/', methods=['GET'])
@login_required
def get_all_watchlists():
    print(current_user)
    try:
        # print(watchlist)
        all_watchlists = models.Watchlist.filter(user=current_user.id)
        # breakpoint()
        watchlists = [model_to_dict(watchlist) for watchlist in all_watchlists]
        return jsonify(data=watchlists, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@watchlist.route('/', methods=['POST'])
@login_required
def create_watchlists():
    # print(current_user)
    # print(request.get_json())
    body = request.get_json()
    # new_watchlist = models.Watchlist.create(**body)
    new_watchlist = models.Watchlist.create(title=body, user=current_user.id, created_at=date.today())
    # print(model_to_dict(new_watchlist))
    watchlist_dict = model_to_dict(new_watchlist)
    return jsonify(data=watchlist_dict, status={'code': 201, "messsage": "Success"})
