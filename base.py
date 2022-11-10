from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

import stripe

from utils.postcodes import PostcodeManager
from config import FLASK_SECRET_KEY, DATABASE_HOST, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, STRIPE_SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = FLASK_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}'

db = SQLAlchemy(app)
db.init_app(app)

bcrypt = Bcrypt(app)

stripe.api_key = STRIPE_SECRET_KEY

login_manager = LoginManager(app)
login_manager.login_view = '/login'
login_manager.login_message = 'Please log in to view this page'
login_manager.login_message_category = 'danger'

postcode_manager = PostcodeManager()
