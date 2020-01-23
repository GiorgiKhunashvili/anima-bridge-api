from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = '\x10n\xef\xb0\xf71\xa4R\xcd\xf3o\xed\xfb\xc7\x95\xe0\xee\xad\xe1\x1a\x12\xc3(V'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

from anima_api import routes
