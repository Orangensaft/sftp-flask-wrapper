from flask import Flask, request, abort
from libs import sftp
app = Flask(__name__)


def _get_path(request_json):
    p = request_json.get("path","")
    return p if p != "" else "."

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/list")
def list_dir():
    """
    {
        "path": "..."
    }
    """
    d = _get_path(request.json)
    return {"contents":sftp.list_dir(d)}


@app.route("/get")
def get_file():
    """
    {
        "path": "foo/bar/baz.log"
    }
    """
    path = _get_path(request.json)
    try:
        return {"contents": sftp.get_file(path)}
    except FileNotFoundError:
        abort(404)


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
