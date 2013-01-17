# Import modules/packages

# Munge our path so we can find the templates
import web
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
service = "gdocs"
singly_access_token = "8qYRI3LcoP4wmVb8Qyc5nVEefLA.JHzADqmFf4b792c19e365d84023cbdb5e77e0c664be366887e4a20b2bb795fa12106f58c81389752db1f89139d063fbcf51d7c36a6395081a8258b182dc761db79ed52dae60ab6c4e0e74a52302aabc827ccfdca6c7d6f54e0596aba2b4363e8f5fd4f90"

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
        url = "https://api.singly.com/oauth/authenticate?client_id={singly_client_id}&redirect_uri={redirect_uri}&service={service}".format(singly_client_id=singly_client_id, redirect_uri=redirect_uri, service=service)
        print url
        web.seeother(url)

class Bouncer:
    def GET (self):
        params = web.input(code=None)
        return params.code

class Export:
    def GET (self):
        url = "https://api.singly.com/profiles?access_token={access_token}".format(access_token=singly_access_token)
        web.seeother(url)




# If this module is called directly, start the app
if __name__ == "__main__":
    # Declare the application
    app = web.application(urls, globals(), autoreload=True)
    app.run()
