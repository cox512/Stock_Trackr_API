import models
from flask import Blueprint, jsonify, request, make_response
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user
from datetime import date
from resources.users import token_required

watchlist = Blueprint('watchlists', 'watchlist')

#SHOW route
@watchlist.route('/<id>', methods=['GET'])
# @token_required
def get_one_watchlist(current_user, id):
    print(id, 'watchlist id')
    watchlist = models.Watchlist.get_by_id(id)
    watchlist_dict = model_to_dict(watchlist)
    # print(watchlist_dict)
    return jsonify(data=watchlist_dict, status={"code": 200, "message": "Success"})


@watchlist.route('/', methods=['GET'])
# @login_required
# @token_required
def get_all_watchlists(current_user):
    print('GET all Watchlists')
    print(current_user.id)
    try:
        # print(watchlist)
        #Filter gets many items, 'get' just gets the first one.
        all_watchlists = models.Watchlist.filter(user=current_user.id)
        print(all_watchlists)
        # breakpoint()
        watchlists = [model_to_dict(watchlist) for watchlist in all_watchlists]
        print(watchlist)
        return jsonify(data=watchlists, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@watchlist.route('/', methods=['POST'])
# @login_required
@token_required
def create_watchlists(current_user):
    print('create_watchlist current user:', current_user.id)
    body = request.get_json()
    print(body)
    # new_watchlist = models.Watchlist.create(**body)
    new_watchlist = models.Watchlist.create(title=body['title'], user=current_user.id, created_at=date.today())
    # new_watchlist = models.Watchlist.create(title=body, user=36, created_at=date.today())
    print("watchlist dict:", model_to_dict(new_watchlist))
    watchlist_dict = model_to_dict(new_watchlist)
    return jsonify(data=watchlist_dict, status={'code': 200, "messsage": "Success"})

#UPDATE ROUTE
@watchlist.route('/<id>', methods=['PUT'])
# @login_required
# @token_required
def update_watchlist(current_user, id):
    body = request.get_json()
    update_query = models.Watchlist.update(**body).where(models.Watchlist.id==id)
    #Always have to perform 'execute' on an update because of the method we're using with the database.
    update_query.execute()
    #After sending the query and executing it, we need 
    update_watchlist=models.Watchlist.get_by_id(id)
    return jsonify(data=model_to_dict(update_watchlist), status={"code": 200, "status": "Watchlist successfully updated."})

#DELETE ROUTE
@watchlist.route('/<id>', methods=['DELETE'])
# @login_required
# @token_required
def delete_watchlist(current_user, id):
    body = id
    print(body)
    #Always check to see what the query is returning. There were difficulties with this call because it was only referencing the object, not returning. "get" actually returns the object.
    print(models.Watchlist.get(models.Watchlist.id==body))
    watchlist_query = models.Watchlist.get(models.Watchlist.id==body).delete_instance(recursive=True)
    return jsonify(data={}, success={"code": 200, "message": "Watchlist successfully deleted"})
