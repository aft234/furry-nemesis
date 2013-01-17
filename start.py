# Import modules/packages
import web, requests, json, urllib2, redis
# Munge our path so we can find the templates
from templates import render
# Redis
db = redis.StrictRedis(host='localhost', port=6379, db=0)

# URL Structures
urls = (
    "/",                "Index",
    "/500",             "ServerError",
    "/connect",         "Connect",
    "/bouncer",         "Bouncer",
    "/export",          "Export",
    "/update",          "Update",
)

singly_client_id = "87f100bac9ebc1794e6db565127a3737"
singly_client_secret = "ca776b492e387af88ffc1afb816df605"
redirect_uri = "http://0.0.0.0:8080/bouncer"
service = "google"
scope = "https://www.googleapis.com/auth/userinfo.profile+https://www.googleapis.com/auth/drive+https://www.googleapis.com/auth/drive.file"

def google_token ():
    tk = db.get("google_token")
    if tk is None:
        return "NO_TOKEN_FOUND"
    return tk

def set_google_token (tk):
    db.set("google_token", tk)

# Classes
class Index:
    def GET (self):
        return "hello"
    def POST (self):
        params = web.input(name=None)
        return "hello {name}".format(name=params.name)

class ServerError:
    def GET (self):
        return render.error()

class Connect:
    def GET (self):
        print redirect_uri
        url = "https://api.singly.com/oauth/authenticate?client_id={singly_client_id}&redirect_uri={redirect_uri}&service={service}&scope={scope}".format(singly_client_id=singly_client_id, redirect_uri=redirect_uri, service=service, scope=scope)
        print url
        web.seeother(url)

class Bouncer:
    def GET (self):
        params = web.input(code=None)
        if params.code is None:
            return "No code found.."

        token_convert_url = "https://api.singly.com/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}&profile=google&auth=true".format(client_id=singly_client_id, client_secret=singly_client_secret, code=params.code)
        r = requests.post(token_convert_url)
        tk = r.json()["profile"]["services"]["google"]["auth"]["access_token"]
        set_google_token(tk)
        return "You are now connected."

class Export:
    def GET (self):
        post_url = "https://www.googleapis.com/upload/drive/v2/files?access_token={access_token}&convert=true".format(access_token=google_token())
        headers = {"content-type": "text/html"}
        r = requests.post(post_url, headers=headers)
        db.set("current_file_id", r.json()["id"])

        f = open("testing.doc", "r")
        text = f.read()
        headers = {"content-type": "multipart/form-data"}
        put_url = "https://www.googleapis.com/upload/drive/v2/files/{id}?access_token={access_token}&convert=true&uploadType=media".format(id=db.get("current_file_id"), access_token=google_token())

        r = requests.put(put_url, data=text, headers=headers)

        return "Exporting...Check your google drive..."

class Update:
    def GET (self):
        file_id = db.get("current_file_id")
        get_url = "https://www.googleapis.com/drive/v2/files/{id}?access_token={access_token}".format(id=file_id, access_token=google_token())

        r = requests.get(get_url)
        download_url = "{original_link}&access_token={access_token}".format(original_link=r.json()["exportLinks"]["text/plain"], access_token=google_token())
        r = requests.get(download_url)
        with open("Untitled.txt", "wb") as code:
            code.write(r.content)

        content_updated = "{original_content}\n\n\n\n\nIMAGINE...a new fact....\nwhattup sonnnn\ndidn't think we could do it could you\nthat.\nis.\nhow.\nwe.\nDO.\n\nBAZINGA!".format(original_content=r.content)

        put_url = "https://www.googleapis.com/upload/drive/v2/files/{id}?access_token={access_token}&convert=true&uploadType=media".format(id=file_id, access_token=google_token())

        headers = {"content-type": "multipart/form-data"}
        r = requests.put(put_url, data=content_updated, headers=headers)

        return "Just updated that biatch. \n\nBut hold up.\n\nIt live updates too.\n\nSay whaaaat.\n\nYeah playa\n\nDidn't see it? Saad...hit that update again for everyone (refresh the page)"


# If this module is called directly, start the app
if __name__ == "__main__":
    # Declare the application
    app = web.application(urls, globals(), autoreload=True)
    app.run()
