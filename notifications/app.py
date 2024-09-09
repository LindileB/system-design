from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'This is the index page of this app', 200