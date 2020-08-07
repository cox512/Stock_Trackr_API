import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

user = Blueprint('users', 'user', url_prefix='/user') #Defines our view functions.

#POST route to register /register
#Temporary to seed a user
@user.route('/', methods=["POST"])
def create_users():
    body = request.get_json()
    print(body)
    user = models.User.create(**body)
    # print(user.__dict__)
    # print(dir(user))
    print(model_to_dict(user), 'model to dict')
    user_dict = model_to_dict(user)
    return jsonify(data=user_dict, status={'code': 201, 'message': 'Success'})


#POST route to login /login

#GET route to logout user /logout



