# Import modules/packages

# Munge our path so we can find the templates
import web, requests, json, urllib2
from templates import render

# URL Structures
urls = (
    "/",                "Index",
    "/500",             "ServerError",
    "/connect",         "Connect",
    "/bouncer",         "Bouncer",
    "/export",          "Export",
)

singly_client_id = "87f100bac9ebc1794e6db565127a3737"
singly_client_secret = "ca776b492e387af88ffc1afb816df605"
redirect_uri = "http://0.0.0.0:8080/bouncer"
service = "google"
scope = "https://www.googleapis.com/auth/userinfo.profile+https://www.googleapis.com/auth/drive+https://www.googleapis.com/auth/drive.file"
singly_access_token = "UvW4HFHbswLQqTdIXl8LJZMfdA4.-vRGOZhTa52672030bb46b49744a964a4acde70e61b4ccfa5d4e65296b4db3687b1ba0b347359873bf3e747f5331eb54a29a7f687297cf897c3f3cf2aec263277b4426c11c194e804361beca62c95ff276d6d36c780c73e9890abb47fe94d5c9b1511afd"
google_singly_access_token = "ya29.AHES6ZT5yMiG8lnHU6wp7x5fFV55Tw9TpJAqE4GDAakdvhZd0XyOWg"

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
        return params.code

class Export:
    def GET (self):
        post_url = "https://www.googleapis.com/upload/drive/v2/files?access_token={access_token}&convert=true".format(access_token=google_singly_access_token)
        print post_url
        data = {
            "title": "testing.doc",
            "description": "Stuff about the file",
            "mimeType": "application/msword"
        }
        headers = {"content-type": "text/html"}
        files = {"file": ("testing.doc", open("testing.doc", "rb"))}
        r = requests.post(post_url, headers=headers)

        file_id = r.json()["id"]
        put_url = "https://www.googleapis.com/upload/drive/v2/files/{id}?access_token={access_token}&convert=true&uploadType=media".format(id=file_id, access_token=google_singly_access_token)
        r = requests.put(put_url, headers=headers, files=files)
        return r.text


# If this module is called directly, start the app
if __name__ == "__main__":
    # Declare the application
    app = web.application(urls, globals(), autoreload=True)
    app.run()
