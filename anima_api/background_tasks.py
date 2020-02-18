from anima_api import celery
from anima_api.models import UserProgress, PageAccess
import time
from anima_api import PAGE_ACCESS_TOKEN, db
import requests
from anima_api.marili import typing_on, typing_off
import json

FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'


def send_message(recipient_id, text):
    """Send a response to Facebook"""
    payload = {
        'message': {
            'text': text
        },
        'recipient': {
            'id': recipient_id
        },
        'notification_type': 'regular'
    }

    auth = {
        'access_token': PAGE_ACCESS_TOKEN
    }

    response = requests.post(
        FB_API_URL,
        params=auth,
        json=payload
    )

    return response.json()


@celery.task()
def combinator(sender_id, pa_token):
    user = UserProgress.query.filter_by(user_id=int(sender_id)).first()
    user.sent = True
    db.session.commit()
    while user.last_date + 4 > int(time.time()):
        print(user.last_date)
        time.sleep(0.5)
        db.session.refresh(user)
    else:
        updated_data = UserProgress.query.filter_by(user_id=int(sender_id)).first()
        typing_on(sender_id, pa_token)
        time.sleep(2)
        typing_off(sender_id, pa_token)
        send_message(updated_data.user_id, updated_data.last_message)
        print(user.last_message)
        user.combine = False
        user.sent = False
        db.session.commit()
        print("message was sent")
        print("sent message")


