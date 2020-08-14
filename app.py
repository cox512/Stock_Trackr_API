import os
from flask import Flask, g, jsonify, session, redirect, url_for, request, make_response
from flask_cors import CORS, cross_origin
from flask_login import LoginManager
from dotenv import load_dotenv
load_dotenv()
import models
from resources.users import user #import the user, stock, and watchlist resources from users.py
from resources.stocks import stock
from resources.watchlists import watchlist
from playhouse.db_url import connect
# from markupsafe import escape

DEBUG = True #Allows error messages to be printed out in the server.
PORT = 8000

login_manager = LoginManager()
app = Flask(__name__)

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE='None',
)

#User Authentication
app.secret_key = os.getenv('SECRET_KEY')
# connect(os.environ.get('DATABASE_URL'))
app.secret_key = 'hoihnkoid'

login_manager.init_app(app)

#This function is a similar concept to Middleware.
@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    """Connect to the db before each request"""
    print("you should see this before each request")
    g.db = models.DATABASE #Sets the db variable to equal our models Database.
    g.db.connect()#Connects app.py to models.py database

@app.after_request #Closes the connection and returns the response
def after_request(response):
    """Close the db connetion after each request"""
    print("you should see this after each request")
    g.db.close()
    return response

#DON'T FORGET TO ADD YOUR HEROKU SITE HERE
CORS(user, origins=['http://localhost:3000', 'https://ten-bagger.herokuapp.com'], supports_credentials=True) #Sets the front-end url, support credentials allows cookies to be set to the server
app.register_blueprint(user, url_prefix='/user') #Sets the handing instructions for our routes.

CORS(stock, origins=['http://localhost:3000', 'https://ten-bagger.herokuapp.com'], supports_credentials=True)
app.register_blueprint(stock, url_prefix='/api/v1/stocks')

CORS(watchlist, origins=['http://localhost:3000', 'https://ten-bagger.herokuapp.com'], supports_credentials=True)
app.register_blueprint(watchlist, url_prefix='/api/v1/watchlists')

if 'ON_HEROKU' in os.environ: 
    print('\non heroku!')
    models.initialize()

if __name__ == '__main__':
    models.initialize() #Calls the initialize function from models.py and initializes the Database
    app.run(debug=DEBUG, port=PORT)