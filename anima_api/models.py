from anima_api import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}'), '({self.email})'"


class PageAccess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bot_id = db.Column(db.Integer)
    page_id = db.Column(db.Integer)
    PA_TOKEN = db.Column(db.String(250))

    def __repr__(self):
        return f"User(id '{self.id}'), 'bot_id ({self.bot_id}), '(page_id {self.page_id})', (user_id {self.user_id})"

    user_id = db.Column(db.Integer)


class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    progress_id = db.Column(db.Integer)
    page_id = db.Column(db.Integer)
    last_message = db.Column(db.String)
    last_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sent = db.Column(db.Boolean, default=False)
    chatbot_message_delivered = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User('id {self.id}'), '(bot_id {self.bot_id}), '(page_id {self.page_id})', (user_id {self.user_id})"

