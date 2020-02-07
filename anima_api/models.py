from anima_api import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}'), '({self.email})'"


class PageAccess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bot_id = db.Column(db.Integer, unique=True)
    page_id = db.Column(db.Integer, unique=True)
    PA_TOKEN = db.Column(db.String(250), unique=True)

    def __repr__(self):
        return f"User(id '{self.id}'), 'bot_id ({self.bot_id}), '(page_id {self.page_id})', (user_id {self.user_id})"

    user_id = db.Column(db.Integer)


class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.BigInteger, unique=True)
    progress_id = db.Column(db.Integer, default=0)
    page_id = db.Column(db.BigInteger, unique=True, nullable=True)
    last_message = db.Column(db.String)
    last_date = db.Column(db.BigInteger)
    sent = db.Column(db.Boolean, default=False)
    combine = db.Column(db.Boolean, default=False)
    chatbot_message_delivered = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User('id {self.id}'), '(page_id {self.page_id})', (user_id {self.user_id})"

