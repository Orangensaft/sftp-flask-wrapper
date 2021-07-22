from flask import Flask, request, abort
from libs import sftp
app = Flask(__name__)


def _get_path(request_json):
    p = request_json.get("path","")
    return p if p != "" else "."


@app.route("/list")
def list_dir():
    """
    {
        "path": "..."
    }
    """
    d = _get_path(request.json)
    try:
        return {"contents":sftp.list_dir(d)}
    except FileNotFoundError:
        abort(404)

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
    except PermissionError:
        abort(403)


@app.route("/put")
def put_file():
    """
    {
        "path": "foo/bar/baz.log",
        "file": "TmV2ZXIgZ29ubmEgZ2l2ZSB5b3UgdXAh"  # Base 64 encoded
    }
    """
    path = _get_path(request.json)
    file = request.json.get("file","")
    try:
        sftp.put_file(path, file)
    except PermissionError:
        abort(403)
    return {"success": True}


@app.route("/del")
def del_file():
    return ""


@app.route("/move")
def move_file():
    return ""

if __name__ == '__main__':
    app.run()
