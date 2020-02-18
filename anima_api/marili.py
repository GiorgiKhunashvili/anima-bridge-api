import json
import requests
from colorama import init, Fore, Back, Style


def get_started(PA_TOKEN):
    data = json.dumps({
        "get_started":{
    "payload":"სალამ"}
    })

    params = {
        "access_token": PA_TOKEN
    }

    headers = {
        "Content-Type": "application/json"
    }

    r = requests.post("https://graph.facebook.com/v2.6/me/messenger_profile",
                      params=params, headers=headers, data=data)
    return r


def typing_on(recipient_id, PA_TOKEN):
    mediaJSON = getSenderActionJSON("typing_on")
    print("# Setting typing " + Fore.GREEN + "ON")
    send_message(recipient_id, PA_TOKEN, mediaJSON)

def typing_off(recipient_id, PA_TOKEN):
    mediaJSON = getSenderActionJSON("typing_off")
    print("# Setting typing " + Fore.MAGENTA + "OFF")
    send_message(recipient_id, PA_TOKEN, mediaJSON)


def mark_seen(recipient_id, PA_TOKEN):
    mediaJSON = getSenderActionJSON("mark_seen")
    print("# Setting Message on"+ Fore.CYAN + "seen")
    send_message(recipient_id, PA_TOKEN, mediaJSON)

def sending_text_handler(recipient_id, message, PA_TOKEN):
    if len(message.split()) != 1:
        if message.find("~") <= 0:
            JSON = getMessageJSON(message)
            send_message(recipient_id, PA_TOKEN, JSON)
            pass
        else:
            message = message + "~"
            if message.find("~") > 0:
                firstPart = message.split("~")
                n = len(firstPart) - 1
                i = 0
                while i < n:
                    JSON = getMessageJSON(firstPart[i])
                    send_message(recipient_id, PA_TOKEN, JSON)
                    i = i + 1
    else:
        JSON = getMessageJSON(message)
        send_message(recipient_id, PA_TOKEN, JSON)

def getSenderActionJSON(typing):
    JSON = {"sender_action": typing}
    return JSON

def getMessageJSON(message):
    JSON = {"message":{
                "text": message}}
    return JSON

class fbCataloge:
    def __init__(self, coverUrl, title, subtitle, url):
        self.coverUrl = coverUrl
        self.title = title
        self.subtitle = subtitle
        self.url = url

    def generateJSON(self):
        catalogeJSON = {"title": self.title,
                 "image_url": self.coverUrl,
                 "subtitle": self.subtitle,
                 "default_action": {
                   "type": "web_url",
                   "url": self.url,
                   "webview_height_ratio": "tall",} }
        return catalogeJSON

def getCatalogeJSON(cataloge):
    JSON = {"message":{
      "attachment":{
        "type":"template",
        "payload":{
          "template_type":"generic",
          "elements": cataloge }
          }
         }
        }
    return JSON

class fbButton():
    def __init__(self, type, payload, title, url):
        self.type = type
        self.url = url
        self.title = title
        self.payload = payload

    def generateJSON(self):
        buttonJSON = {"type": self.type,
                        "url": self.url,
                        "title": self.title,
                        "payload": self.payload
                      }
        return buttonJSON

def getButtonJSON(text, buttons):
    JSON = {"message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"button",
        "text": text,
        "buttons": buttons
      }
    }}}
    return JSON

class fbReply():
    def __init__(self, title, url):
        self.type = "text"
        self.url = url
        self.title = title

    def generateJSON(self):
        qreplyJSON = {
          "content_type":"text",
          "title": self.title,
          "payload":"<POSTBACK_PAYLOAD>",
          "image_url": self.url
        }
        return qreplyJSON

def getReplyJSON(text, qReplies):
    JSON = {"message":{
                "text": text,
                 "quick_replies": qReplies}}
    return JSON

def getUrlJSON(text, url):
    JSON = {"message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"button",
        "text": text,
        "buttons":[
          {
            "type":"web_url",
            "url":url,
            "title": text,
            "webview_height_ratio": "full"
          }
        ]
      }
    }
  }}
    return JSON

def getMultimediaJSON(type, url):
    JSON = {"message":{
                "attachment":{
                  "type": type,
                  "payload":{
                    "url": url,
                  }
                }
              }
            }
    return JSON

def send_message(recipient_id, PA_TOKEN, JSON):
    data = {
        "recipient": {"id": recipient_id},
        }
    data = json.dumps(dict(list(data.items()) + list(JSON.items())))
    print(data)
    params = {
        "access_token": PA_TOKEN
    }

    headers = {
        "Content-Type": "application/json"
    }
    #print(data)
    r = requests.post("https://graph.facebook.com/v4.0/me/messages",
                      params=params, headers=headers, data=data)
    print("# Facebook Callback: " + Fore.CYAN + str(r))

def chatbot_api(bot_id, message_text, contentID, page_id, user_id):
    API_ENDPOINT = "https://animachatbotics.com/ka/FbApi/addword"
    headers = {
        "Content-Type": "application/json"
    }

    # data to be sent to api
    data = {'botId': bot_id,
            'input': message_text,
            'lastBrainPointId': contentID,
            'fbPageId': page_id,
            'dbUserId': user_id}
    data = json.dumps(data)
    # sending post request and saving response as response object
    r = requests.post(url = API_ENDPOINT, data = data, headers = headers)
    print("Sending Data: ", data)
    print("To the API_ENDPOINT: ", API_ENDPOINT)
    print (r)
    # extracting response text
    pastebin_url = r.text
    print("The pastebin URL is:%s"%pastebin_url)
    return r


def send_chatbot_message(message_text, contentID, sender_id, PA_TOKEN, bot_id, page_id):
    try:
        url = "http://5.175.2.145:2121/api/botbot/addword?botId="+str(bot_id)+"&input="+message_text+"&lastBrainPointId="+str(contentID)
        print(url)
        response = requests.post(url)
        entry = response.json()
        print(entry)
        if entry.get("Data"):
            contentID = entry["Data"]["lastBrainPointId"]
            typing_on(sender_id, PA_TOKEN)
            outputs = entry["Data"]["outputs"]
            for output in outputs:
                #print(output)
                output_type = output["type"]
                output_type = int(output_type)
                if output_type == 0:   #text
                    sending_text_handler(sender_id, output["text"], PA_TOKEN)

                elif output_type == 1: #multimedia
                    print("sending multimedia")
                    if output.get("text"):
                      sending_text_handler(sender_id, output["text"], PA_TOKEN)
                    JSON = getMultimediaJSON("image", output["url"])
                    send_message(sender_id, PA_TOKEN, JSON)

                elif output_type == 2: #audio      done
                    print("sending audio")
                    if output.get('text'):
                        sending_text_handler(sender_id, output["text"], PA_TOKEN)
                    JSON = getMultimediaJSON("audio", output["url"])
                    send_message(sender_id, PA_TOKEN, JSON)

                elif output_type == 3: #url      done
                    print("sending URL")
                    JSON = getUrlJSON(output["text"], output["url"])
                    send_message(sender_id, PA_TOKEN, JSON)

                elif output_type == 4: #video      done
                    print("sending video")
                    if output.get('text'):
                        sending_text_handler(sender_id, output["text"], PA_TOKEN)
                    JSON = getMultimediaJSON("video", output["url"])
                    send_message(sender_id, PA_TOKEN, JSON)

                elif output_type == 5: # buttons type, payload, title, url | "web_url","phone_number","postback"
                    buttonsJSON = {}
                    for button in output["buttons"]:
                        if button["type"] == 0:
                            button = fbButton("web_url","",button["title"], button["payload"])
                        elif button["type"] == 1:
                            button = fbButton("phone_number", button["payload"], button["title"], "")
                        elif button["type"] == 2:
                            button = fbButton("postback", button["payload"], button["title"], "")
                        buttonsJSON.setdefault("buttons",[]).append(button.generateJSON())
                    buttonsJSON = getButtonJSON(output["text"], buttonsJSON.get("buttons", ""))
                    send_message(sender_id, PA_TOKEN, buttonsJSON)

                elif output_type == 6: #quick_replies      done
                    replyJSON = {}
                    for reply in output["replies"]:
                        reply = fbReply(reply["title"], "https://www.publicdomainpictures.net/pictures/30000/nahled/solid-green-background.jpg")
                        replyJSON.setdefault("quick_replies",[]).append(reply.generateJSON())
                    replyJSON = getReplyJSON(output["text"], replyJSON.get("quick_replies", ""))
                    send_message(sender_id, PA_TOKEN, replyJSON)

                elif output_type == 7: #cataloge   done
                    print("sending catalog")
                    catalogesJSON = {}
                    for item in output["items"]:
                        catalogeJSON = {}
                        cataloge = fbCataloge(item["coverUrl"], item["title"], item["subtitle"], item["url"])
                        catalogeJSON = cataloge.generateJSON()
                        if item.get("buttons"):
                            buttonsJSON = {}
                            for button in item["buttons"]:
                                button = fbButton(item["title"], item["url"])
                                buttonsJSON.setdefault("buttons",[]).append(button.generateJSON())
                            buttonsJSON = {"buttons": buttonsJSON.get("buttons", "")}
                            catalogeJSON = dict(list(catalogeJSON.items()) + list(buttonsJSON.items()))
                        catalogesJSON.setdefault("cataloges",[]).append(catalogeJSON)
                    catalogesJSON = getCatalogeJSON(catalogesJSON.get("cataloges", ""))
                    send_message(sender_id, PA_TOKEN, catalogesJSON)

                else:
                    pass
        else:
            sending_text_handler(sender_id, "სერვერმა პასუხი არ დააბრუნა", PA_TOKEN) 
        typing_off(sender_id, PA_TOKEN)
        return contentID
    except:
        sending_text_handler(sender_id, "სერვერმა პასუხი არ დააბრუნა", PA_TOKEN) 
        typing_off(sender_id, PA_TOKEN)
        return contentID
