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
    # print(watchlist_dict)
    return jsonify(data=watchlist_dict, status={"code": 200, "message": "Success"})


@watchlist.route('/', methods=['GET'])
@login_required
def get_all_watchlists():
    print(current_user)
    try:
        # print(watchlist)
        #Filter gets many items, 'get' just gets the first one.
        all_watchlists = models.Watchlist.filter(user=current_user.id)
        print(all_watchlists)
        # breakpoint()
        watchlists = [model_to_dict(watchlist) for watchlist in all_watchlists]
        return jsonify(data=watchlists, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@watchlist.route('/', methods=['POST'])
@login_required
def create_watchlists():
    print(current_user)
    body = request.get_json()
    print(body)

    # new_watchlist = models.Watchlist.create(**body)
    new_watchlist = models.Watchlist.create(title=body, user=current_user.id, created_at=date.today())
    # print(model_to_dict(new_watchlist))
    watchlist_dict = model_to_dict(new_watchlist)
    return jsonify(data=watchlist_dict, status={'code': 200, "messsage": "Success"})

#UPDATE ROUTE
@watchlist.route('/<id>', methods=['PUT'])
@login_required
def update_watchlist(id):
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
def delete_watchlist(id):
    #Always check to see what the query is returning. There were difficulties with this call because it was only referencing the object, not returning. "get" actually returns the object.
    watchlist_query = models.Watchlist.get(models.Watchlist.id==id).delete_instance(recursive=True)
    # watchlist_query = models.Watchlist.delete_instance(recursive=True).where(models.Watchlist.id==id)
    # watchlist_query.execute()
    return jsonify(data={}, success={"code": 200, "message": "Watchlist successfully deleted"})
