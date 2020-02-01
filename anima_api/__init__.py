from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
app = Flask(__name__)

app.config['SECRET_KEY'] = '\x10n\xef\xb0\xf71\xa4R\xcd\xf3o\xed\xfb\xc7\x95\xe0\xee\xad\xe1\x1a\x12\xc3(V'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

VERIFY_TOKEN = "4ab1xavav69665VnFvT2u_41VwxXwvgkVsPNeC9afuE"                    # Verification token for Facebook Webhook

from anima_api import routes
