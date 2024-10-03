from http.server import BaseHTTPRequestHandler, HTTPServer, test
from socketserver import ThreadingMixIn
from http.cookies import SimpleCookie
import json
import datetime
import re

class Server(ThreadingMixIn, BaseHTTPRequestHandler):
    req_cnt = 0
    def send_response_only(self, code, message=None):
        if message is None and code in self.responses: message = self.responses[code][0]
        if not hasattr(self, 'response_text'): self.response_text = ''
        self.response_text += ("%s %d %s\r\n" % (self.protocol_version, code, message))
        super().send_response_only(code, message)
    def send_header(self, keyword, value):
        if hasattr(self, 'response_text'): self.response_text += ("%s: %s\r\n" % (keyword, value))
        super().send_header(keyword, value)
    def end_headers(self):
        if hasattr(self, 'response_text'): self.response_text += "\r\n"
        super().end_headers()
    def write(self, s):
        if hasattr(self, 'response_text'): self.response_text += s
        self.wfile.write(s.encode('utf-8'))
    def do_OPTIONS(self): # use to bypass preflight CORS OPTIONS request
        self.send_response(204)
        self.send_header("Access-Control-Allow-Headers", "X-Src")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        return
    def do_GET(self):
        if self.path == '/favicon.ico':
            self.send_response(200)
            self.end_headers()
            return
        if self.path == '/redirect':
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
            return
        Server.req_cnt += 1
        cookies = SimpleCookie(self.headers.get('Cookie'))
        self.send_response(200)
        self.send_header("Ignored-Header", "ignore me")
        self.send_header("Content-type", "text/html")
        csrf = self.headers.get("X-CSRFToken")
        sessionId = 1234
        csrf_cookie = f'{sessionId}-secretcsrf-somerandomsalt-hmac'
        csrf_header = f'my-generated-csrf-token-{csrf_cookie}'
        csrf_head = json.dumps({"X-CSRFToken": csrf_header})
        csrfco = ''
        if 'csrf-cookie' in cookies: csrfco = f'my-generated-csrf-token-{cookies.get("csrf-cookie").value}'.strip()
        name = None
        if 'User-IP' in cookies: name = cookies.get('User-IP').value
        self.send_header('Set-Cookie', f'csrf-cookie={csrf_cookie};SameSite=Strict;Secure;'.replace(' ', ''))
        if self.path == '/':
            self.send_header('Set-Cookie', 'Js-Cookie=true')
            self.end_headers()
            if 'csrf-cookie' in cookies: self.write("<b>Double Cookie CSRF Validated</b>" if csrfco == csrf else "")
            self.write('<script defer src="https://unpkg.com/htmx.org@2.0.2" integrity="sha384-Y7hw+L/jvKeWIRRkqWYfPcvVxHzVzn5REgzbawhxAuQGwX1XWe70vji+VSeHOThJ" crossorigin="anonymous"></script>')
            self.write(f"<body hx-headers='{csrf_head}'><div id='parent'>")
            self.write("<foo>Hello friend</foo>" if not name else f"<foo>Welcome {name}</foo>")
        elif self.path == '/login':
            self.send_header('Set-Cookie', f'User-IP={self.client_address};SameSite=Strict;Secure;HttpOnly;max-age=600'.replace(' ', ''))
            self.end_headers()
            self.write('<script defer src="https://unpkg.com/htmx.org@2.0.2" integrity="sha384-Y7hw+L/jvKeWIRRkqWYfPcvVxHzVzn5REgzbawhxAuQGwX1XWe70vji+VSeHOThJ" crossorigin="anonymous"></script>')
            self.write(f"<body hx-headers='{csrf_head}'><div id='parent'>")
            self.write("<foo>Login</foo>")
        elif self.path == '/hx':
            self.send_header('Hx-Response', 'true')
            self.end_headers()
            self.write(f"<body hx-headers='{csrf_head}'><div id='parent'>")
            if (auth := self.headers.get("Authorization")): self.write(f"<h1>Token: {auth}</h1>")
            if csrf: self.write(f"<i>valid csrf token presented {csrf}</i>")
        self.write("<button hx-get='/hx' hx-target='#parent' hx-swap='outerHTML'>Click me HTMX</button>")
        self.write("</div></body>")

      # log request / response packet
        print(self.command, self.path, self.request_version, self.client_address)
        print("\n" + "="*10 + "Begin" + ">"*10)
        print(self.requestline)
        print(self.headers)
        print('here it will be the request data if presented\r\n')
        print('='*20)
        print("X-CSRFToken", csrf)
        print('csrf-cookie', (t := cookies.get("csrf-cookie")) and t.value, csrfco == csrf)
        print('User Session', name)
        print('='*20)
        print()
        if hasattr(self, 'response_text'): print(self.response_text)
        print("<"*10 + "End" + "="*10)
        

test(Server, HTTPServer, port=8000)
