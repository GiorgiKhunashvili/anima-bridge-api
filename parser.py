import csv
from anima_api.models import PageAccess
from anima_api import db
import time
with open('fb_access.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        bot_id = line[1]
        page_id = line[2]
        PA_TOKEN = line[3]
        user_id = line[4]

        new_pages = PageAccess(bot_id=bot_id, page_id=page_id, USER_ID=user_id, PA_TOKEN=PA_TOKEN)
        db.session.add(new_pages)
        db.session.commit()
