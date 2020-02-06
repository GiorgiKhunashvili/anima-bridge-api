from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from celery import Celery
from flask_migrate import Migrate
app = Flask(__name__)

app.config['SECRET_KEY'] = '764e997f0f5bd60035fa7596d65063581dd22ba6a5891163'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:spongebob109@localhost:5432/anima_api"

# Celery config
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Celery init
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update()

db = SQLAlchemy(app)
migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

# Verification token for Facebook Webhook
VERIFY_TOKEN = "4ab1xavav69665VnFvT2u_41VwxXwvgkVsPNeC9afuE"
PAGE_ACCESS_TOKEN = "EAAPJ755NIeIBAKoekAHntttfaGmtZCJ2PaxsfYwn1jIvr1CJ52AUYolGdIrbMdAej62ZAohbGI6IRbKYMdjq8WiQ" \
                    "2OfGxBkgW7hzA9zKZAXduk0CVxmfrpKqWhHs3CrbSvFNtyFZAAtWKSfrptzNfK8anAl9JxVw9CZBIckqGoQZDZD"


from anima_api import routes
