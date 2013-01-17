# Import modules/packages

# Munge our path so we can find the templates
import web, requests, json
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
singly_access_token = "8zeqaJZPMX_LB3tvDmt_U7rpPhI.jSMipJYM5e757f98c471bf80d07594f87ffe0ca7da0a0c4d6cf75d07c7762c7dcc6ef77461ee6b94acd3b6d90a79ab4f835f752ccfc707279d5bf32eec4483a69e51a99db8f4fd4bd7c2d9efe838790cb22e27302816a0f0eb119f0befd13d8484a78e0c"
google_singly_access_token = "ya29.AHES6ZSsoAwasenVg9du_FjEAayuq6o2ex2-dPG77AThn8IXRaG1lA"

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
        data = {
          "title": "testing.txt",
          "mimeType": "text/plain",
          "description": "Stuff about the file"
        }
        headers = {"content/type": "text/plain"}
        files = {"file": ("testing.txt", open("testing.txt", "rb"))}
        r = requests.post(post_url, data=json.dumps(data), headers=headers)

        print r.text
        file_id = r.json()["id"]
        put_url = "https://www.googleapis.com/upload/drive/v2/files/{id}?access_token={access_token}&convert=true&uploadType=media".format(id=file_id, access_token=google_singly_access_token)
        r = requests.put(put_url, headers=headers, data="shit gets done")
        return r.text


# If this module is called directly, start the app
if __name__ == "__main__":
    # Declare the application
    app = web.application(urls, globals(), autoreload=True)
    app.run()
