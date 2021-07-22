from flask import Flask, request
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/list")
def list_dir():
    return ""


@app.route("/get")
def get_file():
    json = request.json

    return {"ASDF": "f"}


@app.route("/put")
def put_file():
    return ""


@app.route("/del")
def del_file():
    return ""


@app.route("/move")
def move_file():
    return ""

if __name__ == '__main__':
    app.run()
