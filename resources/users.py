import models
from flask import Flask, Blueprint, jsonify, request, session, make_response
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, login_required, current_user, logout_user
# from datetime import date
import jwt 
import datetime
from functools import wraps


user = Blueprint('users', 'user', url_prefix='/user') #Defines our view functions.


app = Flask(__name__)
app.config['SECRET_KEY'] = '02ja22co79b'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print('f:', f)
        print('in token_required')
        # print(*args, **kwargs)
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            print("token:", token)
        if not token:
            return jsonify({'message' : 'token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            print("data:", data)
            current_user= models.User.filter(id=data['id']).first()
            print("current_user:", current_user)
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    
    # print("Got to the end of token-required")
    return decorated

#GET route to check if a user is currently logged in.
@user.route('/', methods=['GET'])
@token_required
# @login_required
def logged_in(current_user):
    # print(model_to_dict(current_user))
    print(current_user)
    if current_user:
        user = [model_to_dict(current_user)]
        return jsonify(data=user, logged_in=True, status={"code": 200, "message": "Success"})
    return "You are not logged in"

#POST route to register /register
@user.route('/register', methods=["POST"])
def create_user():
    auth = request.authorization
    print("auth:", auth)
    body = request.get_json()
    print("body: ", body)
    body['username'] = body['username'].lower()
    try: #Looking for user by username address. If there isn't one, then we move to exception.
        models.User.get(models.User.username == body['username'])
        return jsonify(data={}, status={'code': 401, 'message': 'A user with this username already exists'})
    except models.DoesNotExist: #If the user does not already exist...
        body['password'] = generate_password_hash(body['password'])
        user = models.User.create(**body)
        login_user(user)
        user_dict = model_to_dict(user)
        print(user_dict['id'])
        token = jwt.encode({'id': user_dict['id'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
        print(token)
        #remove the password from returned data
        del user_dict['password']
        return jsonify(data=user_dict, logged_in=True, status={'code': 200, 'message': "Success", 'token': token.decode('UTF-8')})

#SHOW route
@user.route('/<id>', methods=['GET'])
@token_required
def get_one_user(current_user, id):
    print(id, 'this is the id')
    user = models.User.get_by_id(id)
    user_dict = model_to_dict(user)
    print(user_dict)
    return jsonify(data=model_to_dict(user), status={"code": 200, "message": "Success"})

#POST route to login 
@user.route('/login', methods=['POST'])
def login():
    #Use for JWT authorization
    print('login route')
    auth = request.authorization
    print(auth)
    body = request.get_json()
    print("body:", body)
    body['username'] = body['username'].lower()
    try:
        #find the user by username
        user = models.User.get(models.User.username == body['username'])
        #if username found, check the password
        user_dict = model_to_dict(user)
        print("user_dict:", user_dict)
        if check_password_hash(user_dict['password'], body['password']):
            # If correct. Log user in.
            login_user(user)
            print(current_user.username)
            #Create a JSON token for the user
            token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
            del user_dict['password']
             #Sends the user data back from the database so you can use that info on the front side if needed.
            return jsonify(data=user_dict, logged_in=True, status={'code': 200, 'message': 'Success', 'token': token.decode('UTF-8')})
        else:
            return jsonify(data={}, status={'code': 401, 'message': 'Incorrect password'})
    except models.User.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'User does not exist'})

#GET route to logout user
@user.route('/logout', methods=['GET'])
@token_required
# @login_required
def logout(current_user):
    print("current_user: ", current_user)
    logout_user()
    if current_user:
        print("2nd console: ", current_user)
    else:
        print("No current user")
    return jsonify(data={}, status={'code': 200, 'message': 'Successful Logout'})

#UPDATE ROUTE
@user.route('/<id>', methods=['PUT'])
# @login_required
@token_required
def update_user(current_user, id):
# def update_user(id):
    print("put route current_user:", current_user)
    body = request.get_json()
    update_query = models.User.update(**body).where(models.User.id==id)
    #Always have to perform 'execute' on an update because of the method we're using with the database.
    update_query.execute()
    #After sending the query and executing it, we need 
    update_user=models.User.get_by_id(id)
    return jsonify(data=model_to_dict(update_user), status={"code": 200, "status": "User successfully updated."})

#DELETE USER ROUTE 
@user.route('/<id>', methods=['DELETE'])
@token_required
# @login_required
def delete_user(current_user, id):
    print(id)
    user_query = models.User.get(models.User.id==id).delete_instance(recursive=True)
    return jsonify(data={}, success={"code": 200, "message": "User successfully deleted"})



