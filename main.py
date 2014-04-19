import webapp2
from google.appengine.api import urlfetch
import urllib
import urlparse

PASSWORD = "change_me"


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.abort(403, detail="This is a private service.")


class ForwardHandler(webapp2.RequestHandler):
    def post(self):
        self.abort(400, detail="You can only make GET requests to this service.")

    def get(self):
        if not self.request.query_string:
            self.abort(400, detail="Query string required.")

        try:
            if self.request.GET.getone("password") != PASSWORD or PASSWORD == "change_me":
                self.abort(403, detail="Incorrect password. This is a private service.")

            url = self.request.GET.getone("url")
            fields_str = self.request.GET.getone("fields")

        except KeyError:
            self.abort(400, detail="Query string must include 'url', 'fields', and 'password'. See Readme.md.")

        fields_list = urlparse.parse_qsl(fields_str)  # handles multiple values per key just fine (uncommon, but valid)

        result = urlfetch.fetch(url,
                                payload=urllib.urlencode(fields_list),
                                method=urlfetch.POST,
                                deadline=20,
                                validate_certificate=False,  # security schmecurity
                                headers={'Content-Type': 'application/x-www-form-urlencoded'})

        if result.status_code == 200:
            return webapp2.Response(result.content)
        else:
            self.abort(500, detail="Error fetching remote page.")


class BlackMirror(webapp2.RequestHandler):
    def get(self):
        self.response.write("The Black Mirror only responds to HTTP POST requests.")

    def post(self):
        self.response.write('<html><body style="background-color:#000; font-family:monospace; color:#fff">')
        self.response.write('<h1>Black Mirror</h1><h2>Header received:</h2>')
        for k, v in self.request.headers.items():
            self.response.write(k + ": " + v + "<br />")
        self.response.write("<h2>POST fields received:</h2>")
        for k, v in self.request.POST.items():
            self.response.write(k + ": " + v + "<br />")
        self.response.write('</body></html>')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/forward', ForwardHandler),
    ('/blackmirror', BlackMirror)
], debug=True)
