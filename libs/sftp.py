import stat
from datetime import datetime

import pysftp

def getConnection(hostname: str, user: str = None, pw: str = None, check_hostkey:bool=True) -> pysftp.Connection:
    opts = pysftp.CnOpts()
    if not check_hostkey:
        opts.hostkeys = None
    con = pysftp.Connection(host=hostname, username=user, password=pw, cnopts=opts)
    return con

def list_dir(cn: pysftp.Connection, dirname: str = ".") -> [str]:
    out = []
    dirname = dirname.rstrip("/")
    for i in cn.listdir_attr(dirname):
        out.append({
            "filename": i.filename,
            "full_path": f"{dirname}/{i.filename}",
            "is_directory": stat.S_ISDIR(i.st_mode),
            "size_bytes": i.st_size,
            "last_access": datetime.fromtimestamp(i.st_atime),
            "last_modification": datetime.fromtimestamp(i.st_mtime),
            "extension": i.filename.split(".")[-1] if i.filename.count(".") else ""
        })
    return out