# Import modules/packages

# Munge our path so we can find the templates
import sys, os
import web
from templates import render

# URL Structures
urls = (
    "/",     "Index",
    "/500",  "ServerError",
)

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






# If this module is called directly, start the app
if __name__ == "__main__":
    # Declare the application
    app = web.application(urls, globals(), autoreload=True)
    app.run()
