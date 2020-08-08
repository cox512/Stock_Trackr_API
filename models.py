from peewee import *
from flask_login import UserMixin
import datetime

DATABASE = SqliteDatabase('baggr.sqlite') #Creates our SQLite database

class User(UserMixin, Model):
    fname = CharField()
    lname = CharField()
    username = CharField(unique=True) #this will change to ForeignKeyField() I believe
    password = CharField()
    email = CharField(unique=True)
    #watchlists = ForeignKeyField() #I think this is what I have to do in order to get this to reference my watchlists. BUT CAN I CREATE A LIST OFLISTS HERE?
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

class Watchlist(Model): #I'D REALLY RATHER NOT HAVE A WATCHLIST MODEL. I DON'T WANT A MANY TO MANY RELATIONSHIP WITH STOCKS.
    title = CharField()
    user = ForeignKeyField(User, backref='users') #A way of associating a user with a watchlist. This could help overcome our (possible) inability to use a list as a datatype in the user model.
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = DATABASE

class Stock(Model):  #STILL BUILDING THIS. STOCKS AND WATCHLISTS WOULD HAVE A MANY TO MANY RELATIONSHIP.
    company_name = CharField()
    ticker = CharField()
    current_price = FloatField()
    open_price = FloatField()
    close_price = FloatField()
    day_high = FloatField()
    day_low = FloatField()
    volume = IntegerField()
    watchlist = ForeignKeyField(Watchlist, backref='api/v1/watchlists')
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

# class WatchlistStocks(Model): This is the start of a many-to-many model
#     stock = ForeignKeyField(Stock)
#     watchlist = ForeignKeyField(Watchlist)

#     class Meta:
#         database = DATABASE

def initialize(): #Called when initializing the app
    DATABASE.connect() #Connect to DB
    DATABASE.create_tables([User, Stock, Watchlist], safe=True) #Creates the various tables
    print("TABLES Created")
    DATABASE.close() #Closes the connection once initialization has occurred.