# Import modules/packages
import web

# URL Structures
urls = (
    "/",     "Index",
)

# Classes
class Index:
    def GET (self):
        return "hello"
    def POST (self):
        params = web.input(name=None)
        return "hello {name}".format(name=params.name)








# If this module is called directly, start the app
if __name__ == "__main__":
    # Declare the application
    app = web.application(urls, globals(), autoreload=True)
    app.run()
