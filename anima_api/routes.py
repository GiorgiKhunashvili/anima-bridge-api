from anima_api import app
from flask import request, jsonify, render_template, url_for, flash, redirect
from anima_api import VERIFY_TOKEN, db, bcrypt
from colorama import Fore
import requests
from anima_api.background_tasks import combinator
from anima_api.forms import RegistrationForm, LoginForm, CreateAccessPage
from .models import User, UserProgress, PageAccess
from flask_login import login_user, current_user, logout_user, login_required
from anima_api.marili import mark_seen
import csv
from anima_api.models import PageAccess
from anima_api import db
<<<<<<< HEAD
import time
=======

>>>>>>> 052fe66a590f74299a9de0a0207062d3ad66163a

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
<<<<<<< HEAD
    pa_token = PageAccess.query.filter_by(page_id=page_id)
    mark_seen(sender_id, pa_token.PA_TOKEN)
=======
    # pa_token = PageAccess.query.filter_by(page_id=page_id).first()
    # print(pa_token)
    # mark_seen(sender_id, pa_token.PA_TOKEN)
>>>>>>> 052fe66a590f74299a9de0a0207062d3ad66163a
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
<<<<<<< HEAD
            combinator.delay(sender_id, pa_token.PA_TOKEN)
=======
            combinator.delay(sender_id)
>>>>>>> 052fe66a590f74299a9de0a0207062d3ad66163a
    else:
        user_progess = UserProgress(user_id=int(sender_id), page_id=int(page_id), last_message=message,
                                    last_date=int(timestamp/1000))
        db.session.add(user_progess)
        db.session.commit()
        combinator.delay(sender_id)
        print("user was saved")
    return 'ok', 200


@login_required
@app.route('/home', methods=['GET'])
def home():
    pages = PageAccess.query.all()

    return render_template('home.html', pages=pages)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please Check email and password', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html')


@app.route('/page-access/new', methods=['GET', 'POST'])
@login_required
def new_page_access():
    form = CreateAccessPage()
    if form.validate_on_submit():
        page_access = PageAccess(name=form.name.data, bot_id=int(form.bot_id.data), page_id=int(form.page_id.data),
                                PA_TOKEN=form.pa_token.data)
        db.session.add(page_access)
        db.session.commit()
        flash("Page was succesfuly created", 'success')
        return redirect(url_for('home'))
    return render_template('create_page_access.html', form=form, legend='Create new page')


@app.route('/page/<int:id>')
@login_required
def page(id):
    page = PageAccess.query.get_or_404(id)
    return render_template('page.html', page=page)


@app.route('/page/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_page(id):
    page = PageAccess.query.get_or_404(id)
    form = CreateAccessPage()
    if form.validate_on_submit():
        page.name = form.name.data
        page.bot_id = form.bot_id.data
        page.page_id = form.page_id.data
        page.PA_TOKEN = form.pa_token.data
<<<<<<< HEAD
=======
        page.user_id = form.user_id.data
>>>>>>> 052fe66a590f74299a9de0a0207062d3ad66163a
        db.session.commit()
        flash('Page was successfully updated', 'success')
        return redirect(url_for('page', id=page.id))
    elif request.method == "GET":
        form.name.data = page.name
        form.bot_id.data = page.bot_id
        form.page_id.data = page.page_id
        form.pa_token.data = page.PA_TOKEN
<<<<<<< HEAD
=======
        form.user_id.data = page.USER_ID
>>>>>>> 052fe66a590f74299a9de0a0207062d3ad66163a
    return render_template('create_page_access.html', form=form, legend='Update Page')


@app.route('/page/<int:id>/delete', methods=['POST'])
@login_required
def delete_page(id):
    page = PageAccess.query.get_or_404(id)
    db.session.delete(page)
    db.session.commit()
    flash('Page was deleted', 'success')
    return redirect(url_for('home'))


<<<<<<< HEAD
@app.route('/ola')
def charts():
    with open('fb_access.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            bot_id = line[1]
            page_id = line[2]
            PA_TOKEN = line[3]
            user_id = line[4]

            new_pages = PageAccess(bot_id=bot_id, page_id=page_id, user_id=user_id, PA_TOKEN=PA_TOKEN)
            db.session.add(new_pages)
            db.session.commit()
    return redirect(url_for('home'))
=======
# @app.route('/ola')
# def charts():
#     with open('fb_access.csv', 'r') as csv_file:
#         csv_reader = csv.reader(csv_file)
#         for line in csv_reader:
#             bot_id = line[1]
#             page_id = line[2]
#             PA_TOKEN = line[3]
#             user_id = line[4]
#
#             new_pages = PageAccess(bot_id=bot_id, page_id=page_id, USER_ID=user_id, PA_TOKEN=PA_TOKEN)
#             db.session.add(new_pages)
#             db.session.commit()
#     return redirect(url_for('home'))


@app.route('/charts')
def charts():
    return render_template('charts.html')
>>>>>>> 052fe66a590f74299a9de0a0207062d3ad66163a

