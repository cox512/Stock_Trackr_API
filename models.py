from peewee import *
from flask_login import UserMixin
import datetime

DATABASE = SqliteDatabase('baggr.sqlite', pragmas={'foreign_keys': 1}) #Creates our SQLite database. Enforcing foreign_key restraints.

class User(UserMixin, Model):
    fname = CharField()
    lname = CharField()
    username = CharField(unique=True) #this will change to ForeignKeyField() I believe
    password = CharField()
    email = CharField(unique=True)
    #watchlists = ForeignKeyField() #I think this is what I have to do in order to get this to reference my watchlists. 
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

class Watchlist(Model): 
    title = CharField()
    user = ForeignKeyField(User, backref='watchlists') #A way of associating a user with a watchlist. "user-one.watchlists" should give us all the watchlists associated with that user id.
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