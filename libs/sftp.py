import stat
from datetime import datetime
from os import environ
import pysftp

TIME_FORMAT = environ.get("API_TIME_FORMAT", "%Y-%m-%d %H:%M:%S")


def get_settings():
    return {
        "hostname" : environ.get("SFTP_HOST","127.0.0.1"),
        "port": int(environ.get("SFTP_PORT","22")),
        "user": environ.get("SFTP_USERNAME", None),
        "pw": environ.get("SFTP_PASSWORD", None),
        "check_hostkey": not bool(environ.get("SFTP_SKIP_HOSTKEY",False))
    }


def get_connection():
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


def _list_dir(cn: pysftp.Connection, dirname: str = ".") -> [str]:
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