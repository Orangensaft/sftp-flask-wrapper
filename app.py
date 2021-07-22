from flask import Flask, request, abort
from libs import sftp
app = Flask(__name__)


def _get_path(request_json, key="path"):
    p = request_json.get(key,"")
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
    """
    {
        "path": "foo/bar/baz.log"
    }
    """
    path = _get_path(request.json)
    try:
        sftp.delete_file(path)
    except FileNotFoundError:
        abort(404)
    except IOError:
        return {"success": False, "msg": "Could not delete file or directory. Directory could be non-empty or file could be in use"}, 400
    return ""

@app.route("/move")
def move_file():
    """
    {
        "path_src": "foo/bar/baz.log",
        "path_dst": "lorem/ipsum/dolor.log"
    }
    """
    src = _get_path(request.json, "path_src")
    dst = _get_path(request.json, "path_dst")
    if src == dst:
        return ""
    try:
        sftp.move_file(src, dst)
    except FileNotFoundError:
        abort(404)
    except sftp.TargetExistsException:
        return {"success": False, "msg": "Target file already exists"}
    return ""


@app.route("/exists")
def exists():
    """
    {
        "path": "foo/bar/baz.log"
    }
    """
    path = _get_path(request.json)
    if sftp.exists(path):
        return ""
    else:
        return 404


if __name__ == '__main__':
    app.run()
