from flask import Flask, g, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from dotenv import load_dotenv
load_dotenv()

import models
from resources.users import user #import the user, stock, and watchlist resources from users.py
from resources.stocks import stock
from resources.watchlists import watchlist

DEBUG = True #Allows error messages to be printed out in the server.
PORT = 8000

login_manager = LoginManager()
app = Flask(__name__)

#User Authentication
app.secret_key = "SECRETKEY"
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
    g.db = models.DATABASE #Sets the db variable to equal our models Database.
    g.db.connect()#Connects app.py to models.py database

@app.after_request #Closes the connection and returns the response
def after_request(response):
    g.db.close()
    return response

CORS(user, origins=['http://localhost:3000'], supports_credentials=True) #Sets the front-end url, support credentials allows cookies to be set to the server
app.register_blueprint(user, url_prefix='/user') #Sets the handing instructions for our routes.

CORS(stock, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(stock, url_prefix='/api/v1/stocks')

CORS(watchlist, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(watchlist, url_prefix='/api/v1/watchlists')


if __name__ == '__main__':
    models.initialize() #Calls the initialize function from models.py and initializes the Database
    app.run(debug=DEBUG, port=PORT)