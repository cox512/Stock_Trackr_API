import os
import models
from flask import Flask, Blueprint, jsonify, request, session, make_response
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, login_required, logout_user
import jwt 
import datetime
from functools import wraps

user = Blueprint('users', 'user', url_prefix='/users') #Defines our view functions.

SECRET_KEY = os.getenv('SECRET_KEY')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print('in token_required')
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            # print("token:", token)
        if not token:
            return jsonify({'message' : 'token is missing'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            # print("data:", data)
            current_user= models.User.filter(id=data['id']).first()
            # print("current_user:", current_user)
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    
    return decorated

#Check if a user is currently logged in.
@user.route('/', methods=['GET'])
# @login_required
@token_required
def logged_in(current_user):
    print("logged_in session id:", session['id'])
    # print(model_to_dict(current_user))
    # user = models.User.query.filter_by(id=1).first()
    print("current_user:", current_user.username)

    if current_user:
        print("current_user exists")
        # return "Found a user"
        user = [model_to_dict(current_user)]
        return jsonify(data=user, logged_in=True, status={"code": 200, "message": "The user is logged in"})
    return "You are not logged in"

#POST route to register /register
@user.route('/register', methods=["POST"])
def create_user():
    body = request.get_json()
    print("body: ", body)
    body['username'] = body['username'].lower()
    try: 
        models.User.get(models.User.username == body['username'])
        return jsonify(data={}, status={'code': 401, 'message': 'A user with this username already exists'})
    except models.DoesNotExist:
        body['password'] = generate_password_hash(body['password'])
        user = models.User.create(**body)
        login_user(user)
        user_dict = model_to_dict(user)
        print(user_dict['id'])

        token = jwt.encode({'id': user_dict['id'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, SECRET_KEY)
        
        user_dict['token'] = token
        del user_dict['password']

        return jsonify(data=user_dict, logged_in=True, status={'code': 200, 'message': "Success"})

#SHOW route
@user.route('/<id>', methods=['GET'])
@token_required
def get_one_user(current_user, id):
    print(id, 'this is the id')
    user = models.User.get_by_id(id)
    user_dict = model_to_dict(user)
    print(user_dict)
    return jsonify(data=model_to_dict(user), status={"code": 200, "message": "Success"})

#Login route 
@user.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    body['username'] = body['username'].lower()
    try:
        user = models.User.get(models.User.username == body['username'])
        user_dict = model_to_dict(user)
        if check_password_hash(user_dict['password'], body['password']):
            login_user(user, remember=True)

            token = jwt.encode({'id': user_dict['id'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, SECRET_KEY)
            
            user_dict['token'] = token
            del user_dict['password']
            return jsonify(data=user_dict, logged_in=True, status={'code': 200, 'message': 'Success'}) 
        else:
            return jsonify(data={}, status={'code': 401, 'message': 'Incorrect password'})
    except models.User.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'User does not exist'})

#GET route to logout user
@user.route('/logout', methods=['GET'])
# @login_required
def logout():
    logout_user()
    return jsonify(data={}, status={'code': 200, 'message': 'Successful Logout'})

#UPDATE ROUTE
@user.route('/<id>', methods=['PUT'])
@token_required
def update_user(current_user, id):
    user_id = id
    print("delete route current_user:", user_id)
    body = request.get_json()
    update_query = models.User.update(**body).where(models.User.id==user_id)
    #Always have to perform 'execute' on an update because of the method we're using with the database.
    update_query.execute()
    
    update_user=models.User.get_by_id(user_id)
    return jsonify(data=model_to_dict(update_user), status={"code": 200, "status": "User successfully updated."})

#DELETE USER ROUTE 
@user.route('/<id>', methods=['DELETE'])
@token_required
def delete_user(current_user, id):
    user_id = id
    print("delete user:", user_id)
    user_query = models.User.get(models.User.id==user_id).delete_instance(recursive=True)
    logout_user()
    return jsonify(data={}, success={"code": 200, "message": "User successfully deleted"})



