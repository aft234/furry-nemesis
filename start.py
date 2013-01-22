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
    "/test",            "Test",
    "/tokens",          "Tokens",
    "/clean",           "Clean"
)

singly_client_id = "0e1514c50a95b214f13567123dc23e87"
singly_client_secret = "6760198d31e33e65466620095fadfefc"
google_client_id = "366462171286.apps.googleusercontent.com"
google_client_secret = "EKDKiG9U1O3xN3oigVe2Q-zr"
redirect_uri = "http://0.0.0.0:8080/bouncer"
service = "google"
scope = "https://www.googleapis.com/auth/userinfo.profile+https://www.googleapis.com/auth/drive+https://www.googleapis.com/auth/drive.file+https://www.google.com/analytics/feeds/"

def google_token ():
    print "Fetching google access token"
    tk = db.get("google_token")
    if tk is None:
        print "Attempting to refresh old access token"
        refresh = db.get("google_refresh_token")
        # Refresh the tokenz
        r = requests.post("https://accounts.google.com/o/oauth2/token", {
            "refresh_token" : refresh,
            "client_id" : google_client_id,
            "client_secret" : google_client_secret,
            "grant_type" : "refresh_token"
        })
        set_google_token(**r.json())
        tk = db.get("google_token")
    print "Returning {token}".format(token=tk)
    return tk

def set_google_token (access_token=None, refresh_token=None, expires_in=None, **kwargs):
    db.set("google_token", access_token)
    db.expire("google_token", int(expires_in) - 100)
    if refresh_token is not None:
        db.set("google_refresh_token", refresh_token)

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

class Tokens:
    def GET (self):
        return json.dumps({ "access_token" : google_token(), "refresh_token" : db.get("google_refresh_token") })

class Clean:
    def GET (self):
        db.set("google_token", None)
        db.set("google_refresh_token", None)
        return "Removed all tokens"

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
        blob = r.json()
        set_google_token(**blob["profile"]["services"]["google"]["auth"])
        return r.text

class Test:
    def GET (self):
        url = "https://www.googleapis.com/analytics/v3/management/segments?access_token={token}".format(token=google_token())
        r = requests.get(url)
        return r.text
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
