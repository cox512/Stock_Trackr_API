import models
from flask import Blueprint, jsonify, request
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, login_required, current_user

user = Blueprint('users', 'user') #Defines our view functions.


#GET route to display users -- used for development and to check connections.
@user.route('/', methods=['GET'])
def get_all_users():
    try:
        users = [model_to_dict(user) for user in models.User.select()]
        print(users)
        return jsonify(data=users, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

#POST route to register /register
@user.route('/register', methods=["POST"])
def create_user():
    body = request.get_json()
    # print(body)
    body['username'] = body['username'].lower()
    try: #Looking for user by username address. If there isn't one, then we move to exception.
        models.User.get(models.User.username == body['username'])
        return jsonify(data={}, status={'code': 401, 'message': 'A user with this username already exists'})
    except models.DoesNotExist: #If the user does not already exist...
        body['password'] = generate_password_hash(body['password'])
        user = models.User.create(**body)
        login_user(user)
        user_dict = model_to_dict(user)
        #remove the password from returned data
        del user_dict['password']
        return jsonify(data=user_dict, status={'code': 200, 'message': "Success"})

#POST route to login /login
@user.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    body['username'] = body['username'].lower()
    try:
        #find the user by username
        user = models.User.get(models.User.username == body['username'])
        #if username found, check the password
        user_dict = model_to_dict(user)
        if check_password_hash(user_dict['password'], body['password']):
                #correct. Log user in.
                login_user(user)
                #Sends the user data back from the database so you can use that info on the front side if needed.
                del user_dict['password']
                return jsonify(data=user_dict, status={'code': 200, 'message': 'Success'})
        else:
            return jsonify(data={}, status={'code': 401, 'message': 'Incorrect password'})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'User does not exist'})

#GET route to logout user /logout



