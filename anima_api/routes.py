from anima_api import app
from flask import request, jsonify, render_template, url_for, flash, redirect
from anima_api import VERIFY_TOKEN, db, bcrypt, PAGE_ACCESS_TOKEN
from colorama import Fore
import requests
from anima_api.background_tasks import combinator
from anima_api.forms import RegistrationForm, LoginForm
from .models import User, UserProgress
from anima_api import celery
import time


@app.route('/', methods=['GET'])
def verify():
    """# Following code will execute after getting GET request from Facebook"""
    # Once the endpoint is added as a webhook, it must return back
    # the 'hub.challenge' value it receives in the request arguments
    if request.args.get('hub.verify_token', '') == VERIFY_TOKEN:
        print("# Connection To Facebook Webhook: " + Fore.GREEN + "[Verified]")
        return request.args.get('hub.challenge', '')
    else:
        print("# Connection To Facebook Webhook: " + Fore.RED + "[Declined]")
        print(Fore.RED + "$ Error: " + Fore.CYAN + "Wrong verification token")
        return "Error, Verification Failed"


@app.route('/WCAPI', methods=['POST'])
def wcapi_messages():
    """ # Following code will execute after getting POST request from Facebook"""
    global WCAPI_contentID
    print(Fore.GREEN + "________________________________________")
    print("# Recieved new message from " + Fore.CYAN + "WebChatAPI")
    data = request.get_json(force=True)
    print(data)
    bot_id = data['botid']
    entry = data['message']
    print(entry)
    print(WCAPI_contentID)
    url = "http://5.175.2.145:2121/api/botbot/addword?botId=" + str(bot_id)+"&input="+entry+"&lastBrainPointId=" +\
          str(WCAPI_contentID)
    print(url)
    response = requests.post(url)
    entry = response.json()
    if entry.get("Data"):
        WCAPI_contentID = entry["Data"]["lastBrainPointId"]
        outputs = entry["Data"]["outputs"]
        ret_array = str(outputs)
        ret_array = ret_array.replace("'", '"')
        print(WCAPI_contentID)
        print(ret_array)
        return jsonify(ret_array)
    else:
        return "An internal error occured", 500


@app.route('/', methods=['POST'])
def handle_messages():
    """Following code will execute after getting POST request from Facebook"""
    print(Fore.GREEN + "________________________________________")
    print("# Recieved new message from " + Fore.CYAN + "Facebook")
    data = request.get_json()
    print(data)
    sender_id = data['entry'][0]['messaging'][0]['sender']['id']
    page_id = data['entry'][0]['messaging'][0]['recipient']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']
    timestamp = data['entry'][0]['messaging'][0]['timestamp']
    if db.session.query(UserProgress).filter_by(user_id=int(sender_id)).scalar() is not None:
        user = UserProgress.query.filter_by(user_id=int(sender_id)).first()
        if user.combine:
            old_text = user.last_message
            user.last_message = old_text + " " + message
        else:
            user.last_message = message
        user.last_date = int(timestamp/1000)
        user.combine = True
        db.session.commit()
        print(user.last_message)
        if user.sent:
            pass
        else:
            combinator.delay(sender_id)
    else:
        user_progess = UserProgress(user_id=int(sender_id), page_id=int(page_id), last_message=message,
                                    last_date=int(timestamp/1000))
        db.session.add(user_progess)
        db.session.commit()
        combinator.delay(sender_id)
        print("user was saved")
    return 'ok', 200


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    return render_template('login.html', form=form)
