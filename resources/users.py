import models
from flask import Blueprint, jsonify, request, session, make_response
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, login_required, current_user, logout_user
# from jinja import escape, Markup


user = Blueprint('users', 'user') #Defines our view functions.


#GET route to check if a user is currently logged in.
@user.route('/', methods=['GET'])
def logged_in():
    print(model_to_dict(current_user))
    print(current_user)
    # try:
    if current_user:
        user = [model_to_dict(current_user)]
        return jsonify(data=user, logged_in=True, status={"code": 200, "message": "Success"})
    return "You are not logged in"

    # except models.DoesNotExist:
    #     return jsonify(data={}, status={"code": 401, "message": "Error getting the current user"})

#POST route to register /register
@user.route('/register', methods=["POST"])
def create_user():
    body = request.get_json()
    print(type(body))
    print(body)
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
        return jsonify(data=user_dict, logged_in=True, status={'code': 200, 'message': "Success"})

#SHOW route
@user.route('/<id>', methods=['GET'])
def get_one_user(id):
    print(id, 'this is the id')
    user = models.User.get_by_id(id)
    user_dict = model_to_dict(user)
    print(user_dict)
    return jsonify(data=model_to_dict(user), status={"code": 200, "message": "Success"})

#POST route to login 
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
            # Set a same-site cookie for first-party contexts - TESTING
            # resp = make_response('Hello, World!')
            # print(resp)
            # resp.headers.add('Set-Cookie','cookie2=value2; SameSite=None; Secure')
            # resp.set_cookie('cookie2', 'value2', samesite='None', secure=True)
            # print(current_user.username)

                #Sends the user data back from the database so you can use that info on the front side if needed.
            del user_dict['password']

            return jsonify(data=user_dict, logged_in=True, status={'code': 200, 'message': 'Success'})
        else:
            return jsonify(data={}, status={'code': 401, 'message': 'Incorrect password'})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'User does not exist'})

#GET route to logout user /logout -- it's a GET because we're basically just getting the route so the logout_user import can do it's dirty work.
@user.route('/logout', methods=['GET'])
@login_required
def logout():
    print("1st console: ", current_user)
    logout_user()
    if current_user:
        print("2nd console: ", current_user)
    else:
        print("No current user")
    return jsonify(data={}, status={'code': 200, 'message': 'Successful Logout'})

#UPDATE ROUTE
@user.route('/<id>', methods=['PUT'])
@login_required
def update_user(id):
    body = request.get_json()
    update_query = models.User.update(**body).where(models.User.id==id)
    #Always have to perform 'execute' on an update because of the method we're using with the database.
    update_query.execute()
    #After sending the query and executing it, we need 
    update_user=models.User.get_by_id(id)
    return jsonify(data=model_to_dict(update_user), status={"code": 200, "status": "User successfully updated."})

#DELETE USER ROUTE
@user.route('/<id>', methods=['DELETE'])
def delete_user(id):
    user_query = models.User.delete().where(models.User.id==id)
    user_query.execute()
    return jsonify(data={}, success={"code": 200, "message": "User successfully deleted"})



