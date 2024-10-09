from http.server import SimpleHTTPRequestHandler, test, HTTPServer
import base64
import os
import random, string

class AuthHTTPRequestHandler(SimpleHTTPRequestHandler):
    _auth = base64.b64encode("admin:admin".encode()).decode()
    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="My Realm rundvrun"')
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """ Present frontpage with user authentication. """
        if self.headers.get("Authorization") == None:
            self.do_AUTHHEAD()
            self.wfile.write(b"no auth header received")
        elif self.headers.get("Authorization") == "Basic " + self._auth:
            SimpleHTTPRequestHandler.do_GET(self)
            password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(32))
            AuthHTTPRequestHandler._auth = base64.b64encode(f"admin:{password}".encode()).decode()
            print(password)
        else:
            self.do_AUTHHEAD()
            #self.wfile.write(self.headers.get("Authorization").encode())
            self.wfile.write(b"not authenticated")

test(AuthHTTPRequestHandler, HTTPServer, port=8000)
