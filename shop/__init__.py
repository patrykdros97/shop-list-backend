from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/mac-patryk/Dev/shop_backend/shop/test.db'
db = SQLAlchemy(app)

from shop.products import models, routes