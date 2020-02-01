from anima_api import app
from flask import request, jsonify
from anima_api import VERIFY_TOKEN
from colorama import Fore
import requests
from .models import PageAccess
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
    print("# JSON package has been " + Fore.GREEN + "[SENT]" + Fore.RESET + " to " + Fore.CYAN + "WebChat")


@app.route('/', methods=['POST'])
def handle_messages():
    """Following code will execute after getting POST request from Facebook"""
    print(Fore.GREEN + "________________________________________")
    print("# Recieved new message from " + Fore.CYAN + "Facebook")
    data = request.get_json()
    print(data)
    return 'ok', 200

#
# @app.route('/facebook', methods=['POST'])
# def my_test_endpoint():
#     data = request.get_json(force=True)
#     entry = data['entry'][0]
#     if entry.get("messaging"):
#         messaging_event = entry['messaging'][0]  # Gets the whole Message
#         sender_id = messaging_event['sender']['id']  # Gets the sender ID
#         page_id = messaging_event['recipient']['id']
#         user = PageAccess.query.filter_by(page_id=page_id).first()
#         pa_token = user.PA_TOKEN
#         bot_id = user.bot_id
#         print("# Sender ID: " + Fore.CYAN + sender_id)
#         print("# Page ID: " + Fore.CYAN + page_id)
#         print("# Time Delievered: " + Fore.CYAN + str(time.strftime("%d %b %Y %H:%M:%S")))
#         if messaging_event.get("message"):
#             if messaging_event['message'].get('text'):
#                 message_text = messaging_event['message']['text']
#                 if len(message_text) >= 250:
#                     message_text = "ფრანჩესკოტოტი"
#                 contentID = dtbs.getUser(int(sender_id), message_text, page_id)
#                 print("# Last Content ID: " + Fore.CYAN + str(contentID))
#                 print("# Message Text: " + message_text)
#                 print("# Bot ID: ", bot_id)
#                 machvibrery.mark_seen(sender_id, PA_TOKEN)
#                 # contentID = machvibrery.send_chatbot_message(message_text, contentID, sender_id, PA_TOKEN, bot_id)
#                 print("# New Content ID: " + Fore.CYAN + str(contentID))
#                 dtbs.addContentID(int(sender_id), int(contentID), message_text, page_id)
#         elif messaging_event.get("postback"):
#             message_text = messaging_event["postback"]["payload"]
#             contentID = dtbs.getUser(int(sender_id), message_text, page_id)
#             print("# Last Content ID: " + Fore.CYAN + str(contentID))
#             print("# Message Text: " + message_text)
#             machvibrery.mark_seen(sender_id, PA_TOKEN)
#             # contentID = machvibrery.send_chatbot_message(message_text, contentID, sender_id, PA_TOKEN, bot_id)
#             dtbs.addContentID(int(sender_id), int(contentID), message_text, page_id)
#
#     return 'ok', 200