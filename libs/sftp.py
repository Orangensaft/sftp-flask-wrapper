import stat
from datetime import datetime
from io import BytesIO
from os import environ
import pysftp
import base64
TIME_FORMAT = environ.get("API_TIME_FORMAT", "%Y-%m-%d %H:%M:%S")


def get_settings() -> dict:
    return {
        "hostname" : environ.get("SFTP_HOST","127.0.0.1"),
        "port": int(environ.get("SFTP_PORT","22")),
        "user": environ.get("SFTP_USERNAME", None),
        "pw": environ.get("SFTP_PASSWORD", None),
        "check_hostkey": not bool(environ.get("SFTP_SKIP_HOSTKEY",False))
    }


def get_connection() -> pysftp.Connection:
    s = get_settings()
    return _getConnection(**s)

def _getConnection(hostname: str, port:int=22, user: str = None, pw: str = None, check_hostkey:bool=True) -> pysftp.Connection:
    opts = pysftp.CnOpts()
    if not check_hostkey:
        opts.hostkeys = None
    con = pysftp.Connection(host=hostname, port=port, username=user, password=pw, cnopts=opts)
    return con


def list_dir(dirname: str = ".") -> [dict]:
    con = get_connection()
    return _list_dir(con, dirname)


def _list_dir(cn: pysftp.Connection, dirname: str = ".") -> [dict]:
    out = []
    dirname = dirname.rstrip("/")
    for i in cn.listdir_attr(dirname):
        out.append({
            "filename": i.filename,
            "full_path": f"{dirname}/{i.filename}",
            "is_directory": stat.S_ISDIR(i.st_mode),
            "size_bytes": i.st_size,
            "last_access": datetime.fromtimestamp(i.st_atime).strftime(TIME_FORMAT),
            "last_modification": datetime.fromtimestamp(i.st_mtime).strftime(TIME_FORMAT),
            "extension": i.filename.split(".")[-1] if i.filename.count(".") else ""
        })
    return out


def get_file(path) -> str:
    return _get_file(get_connection(), path)


def _get_file(con: pysftp.Connection, path: str) -> str:
    out = BytesIO()
    con.getfo(path, out)
    out.seek(0)
    encoded = base64.b64encode(out.read())
    return encoded.decode("utf8")


def put_file(path: str, file: str) -> None:
    _put_file(get_connection(), path, file)


def _get_parent_dir(path: str):
    if path.count("/") == 0:
        return "./"
    else:
        return path.rsplit("/",1)[0]


def _put_file(con: pysftp.Connection, path: str, file: str) -> None:
    file_bytes = base64.b64decode(file.encode("utf8"))
    buffer = BytesIO(file_bytes)
    # We don't want to overcomplicate things, automatically create parent dirs
    con.makedirs(_get_parent_dir(path))
    con.putfo(buffer, path)


def _delete_file(con: pysftp.Connection, path: str) -> None:
    if con.isdir(path):
        # Delete directory
        con.rmdir(path)
    else:
        # Delete a file
        con.remove(path)


def delete_file(path: str) -> None:
    _delete_file(get_connection(), path)


class TargetExistsException(Exception):
    pass


def _move_file(con: pysftp.Connection, src: str, dst: str) -> None:
    if con.exists(dst):
        raise TargetExistsException()
    # check if target parent dirs exist
    parent = _get_parent_dir(dst)
    if not con.exists(parent):
        con.makedirs(parent)

    con.rename(src, dst)


def move_file(src: str, dst: str) -> None:
    _move_file(get_connection(), src, dst)


def _exists(con: pysftp.Connection, path: str) -> bool:
    return con.exists(path)


def exists(path) -> bool:
    return _exists(get_connection(), path)