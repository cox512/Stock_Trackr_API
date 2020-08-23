import os
from peewee import *
from flask_login import UserMixin
import datetime
from playhouse.db_url import connect

if 'ON_HEROKU' in os.environ:
    DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
    DATABASE = SqliteDatabase('baggr.sqlite', pragmas={'foreign_keys': 1}) #Creates our SQLite database. Enforcing foreign_key restraints.

class User(UserMixin, Model):
    #EVENTUALLY YOU SHOULD CREATE A PUBLIC_ID FOR THE USERS, SO IT'S NOT AN EASY SEQUENTIAL GUESS
    #ADD AN OPTION "ADMIN" KEY TO DENOTE IF A USER IS AN ADMIN OR NOT. THIS COULD COME IN HANDY FOR THE TEMPLATE WEBSITE AS WELL. THE USER CAN TEST OUT THE FORMS WITHOUT THEM BEING SAVED TO THE ACTUAL SITE UNLESS THEY HAVE ADMIN PRIVELEDGES.
    fname = CharField()
    lname = CharField()
    username = CharField(unique=True) #this will change to ForeignKeyField() I believe
    password = CharField()
    email = CharField(unique=True) 
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

class Watchlist(Model): 
    title = CharField()
    user = ForeignKeyField(User, on_delete="CASCADE",backref='watchlists') #A way of associating a user with a watchlist. "user-one.watchlists" should give us all the watchlists associated with that user id.
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = DATABASE

class Stock(Model):  
    # company_name = CharField(null=True)
    ticker = CharField()
    watchlist = ForeignKeyField(Watchlist, on_delete="CASCADE", backref='stocks') #See the watchlist model's notes.
    
    class Meta:
        database = DATABASE

def initialize(): #Called when initializing the app
    DATABASE.connect() #Connect to DB
    DATABASE.create_tables([User, Stock, Watchlist], safe=True) #Creates the various tables
    print("TABLES Created")
    DATABASE.close() #Closes the connection once initialization has occurred.