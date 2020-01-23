from anima_api import app
from flask import request


@app.route('/', methods=['POST'])
def hello_world():
    context = request.get_json()
    print(context)
    return "hello world"
