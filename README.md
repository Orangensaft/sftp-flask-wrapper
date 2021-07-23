# sftp-flask-wrapper
Lightweight Flask application to act as a wrapper/proxy for sftp servers. Instead of needing to integrate a sftp library into your software you can instead use this wrapper. You can now interact with the sftp server with a RESTful API.

This is on purpose not trying to completely mirror all operations there are for sftp servers. I'm rather trying to stick to the most used operations:
* Uploading files
* Downloading files
* Moving files within the server
* Deleting files
* Listing files

If there is an important operation missing feel free to open a pull request or open an issue if you want me to implement it.

**The app should already be pretty stable if you are not doing too crazy stuff. Expect an occasional Error 500 on some rare edge cases.**

## Security considerations
Currently the api has **no authentication**, meaning whoever can access the api has access to the sftp server. 

## Setup
First setup your environment with `pipenv sync`. You may also checkout the packages in Pipfile and install manually.

Create a `.env` file next to the `app.py`:
```
SFTP_HOST=127.0.0.1
SFTP_PORT=22
SFTP_USERNAME=foo
SFTP_PASSWORD=pass
SFTP_SKIP_HOSTKEY=1
API_TIME_FORMAT="%Y-%m-%d %H:%M:%S"
```
|Key          |Description|
|-------------|-----------|
|SFTP_HOST    |Host of the sftp server|
|SFTP_PORT    |Port that the sftp server listens on|
|SFTP_USERNAME|Username for sftp auth|
|SFTP_PASSWORD|Password for sftp auth|
|SFTP_SKIP_HOSTKEY|If true hostkey to sftp server will not be checked*|
|API_TIME_FORMAT|Python dateformat string to the list dir command|

**Note:** Usually you should not disable hostkey checking. Make sure to have the hostkey for the sftp already on the machine running this app.

**You are now good to go!** Run the flask app in a way of your liking. Use `flask run` for a quick and dirty setup if you are not planning to use this in a production system.

## API Calls
All calls use `GET`. Use `application/json` as content type.
### Listing a directory
This will list the contents of a directory. Just provide the path as follows:
```
GET /list
{
    "path": "foo/bar"
}
```
**Example Response**
```
200 OK
{
    "contents": [
        {
            "extension": "bmp",
            "filename": "bitmap_file.bmp",
            "full_path": "foo/bar/bitmap_file.bmp",
            "is_directory": false,
            "last_access": "2021-07-22 19:49:02",
            "last_modification": "2021-07-22 19:49:02",
            "size_bytes": 1234
        },
        {
            "extension": "",
            "filename": "Some_Folder",
            "full_path": "foo/bar/Some_Folder",
            "is_directory": true,
            "last_access": "2021-07-22 20:08:55",
            "last_modification": "2021-07-22 19:49:06",
            "size_bytes": 4096
        },
        ...
    ]
}
```
The returned fields should be self-explanatory 😊

**Status 404** will be raised if the directory cannot be found.

### Downloading a file
This will download a given file. Just provide the path as follows:
```
GET /get
{
    "path": "foo/bar/baz.bin"
}
```
This will return the file base64-encoded in a response:
```
{
    "contents": "TmV2ZXIgZ29ubmEgZ2l2ZSB5b3UgdXAh"
}
```
If a file is not found **Status 404** will be returned.

### Uploading a file
To upload a file, provide the base64 encoded file and the target path. **Note:** To keeps things as simple as possible, non-existing parent directories are created automatically.
```
GET /put
{
    "path": "foo/bar/baz.log",
    "file": "TmV2ZXIgZ29ubmEgbGV0IHlvdSBkb3duIQ=="
}
```
Response:
```
{
    "success": true
}
```
If you do not have permissions on the sftp server to upload a file to the given path, **status 403** will be returned.

### Deleting a file/directory
To delete a file or a directory you just have to provide the path. If you are deleting a directory, you have to make sure it's empty first.
```
GET /del
{
    "path": "foo/bar/baz.log"
}
```
On success, status 200 will be returned. If the file/directory was not found status 404 will be returned. A status 400 indicates that the file may not be deleted. This could be because you are trying to delete a non-empty directory or a file that is in use.

### Moving / renaming files
To move or rename a file, provide the source and the destination path:
```
GET /move
{
    "path_src": "foo/bar/baz.log",
    "path_dst": "foo/baz/bar.log"
}
```
This will move the file from foo/bar to foo/baz and at the same time rename it to bar.log.

On success, status 200 will be returned. Status 404 indicates that the source file was not found. Status 400 signals that the target file already exists.

**Note:** again, to keep things simple any missing parent directories for the target path will be created automatically.

### Checking if a file exists
```
GET /exists
{
    "path": "foo/bar/baz.log"
}
```
This will just return status 200 if a file exists and 404 if not.

#Planned features
- [ ] API authentication
- [ ] Supporting SFTPs with public key auth
- [ ] Implementing a proxy mode where instead of using setup sftp credentials they may be provided in every api call to interface with different sftp servers
- [ ] API calls for batch downloading and uploading files
