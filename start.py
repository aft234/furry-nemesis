# Import modules/packages

# Munge our path so we can find the templates
import web, requests, json, urllib2, redis
from templates import render

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
singly_access_token = "UvW4HFHbswLQqTdIXl8LJZMfdA4.-vRGOZhTa52672030bb46b49744a964a4acde70e61b4ccfa5d4e65296b4db3687b1ba0b347359873bf3e747f5331eb54a29a7f687297cf897c3f3cf2aec263277b4426c11c194e804361beca62c95ff276d6d36c780c73e9890abb47fe94d5c9b1511afd"

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
        return google_token()

class Export:
    def GET (self):
        post_url = "https://www.googleapis.com/upload/drive/v2/files?access_token={access_token}&convert=true".format(access_token=google_token())
        print post_url
        payload = {
            "title": "testing.doc",
            "description": "Stuff about the file",
            "mimeType": "application/msword"
        }

        headers = {"content-type": "text/html"}

        r = requests.post(post_url, headers=headers)
        file_id = r.json()["id"]

        f = open("testing.doc", "r")
        text = f.read()

        headers = {"content-type": "multipart/form-data"}
        put_url = "https://www.googleapis.com/upload/drive/v2/files/{id}?access_token={access_token}&convert=true&uploadType=media".format(id=file_id, access_token=google_token())

        r = requests.put(put_url, data=text, headers=headers)
        return r.text

class Update:
    def GET (self):
        file_id = "1gjUJpdZqp7W5LsF0Hhk26jtEIEVAmBc5MN5R3pS4fV8"
        get_url = "https://www.googleapis.com/upload/drive/v2/files/{id}?access_token={access_token}".format(id=file_id, access_token=google_token())

        r = requests.get(get_url)
        return r.text

# If this module is called directly, start the app
if __name__ == "__main__":
    # Declare the application
    app = web.application(urls, globals(), autoreload=True)
    app.run()
