from flask import Flask, request
from libs import sftp
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/list")
def list_dir():
    """
    {
        "directory": "..."
    }
    """
    d = request.json.get("directory",".")
    if d.strip() == "":
        d = "."
    return {"contents":sftp.list_dir(d)}


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
