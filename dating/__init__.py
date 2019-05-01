from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
#from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from config import Config   #from config module, import config class

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(Config) #tells flask to use and apply the config file

    db = SQLAlchemy(app) #db object that represents the database.
    bcrypt = Bcrypt(app) #password hashing function
    login = LoginManager(app) #initializes the flask-login extension
    migrate = Migrate(app, db) #object that represents the migration engine.

#bootstrap = Bootstrap()
    login.login_view = 'login'


from dating import routes, models
#importing a new module called models at the bottom. This module will define the structure of the database.

def main():
    db.create_all()
