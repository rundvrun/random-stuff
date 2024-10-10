from http.server import BaseHTTPRequestHandler, HTTPServer, test
from socketserver import ThreadingMixIn
import random, string, base64, re, subprocess
from ratelimit import limits
import brotli

pattern = re.compile(b"[A-F0-9]+")
AUTHOR = 'rundvrun'
MAX_SIZE_BODY = 5 << 20 # 5MB

class Server(ThreadingMixIn, BaseHTTPRequestHandler):
    _auth = base64.b64encode(f"{AUTHOR}:{AUTHOR}".encode()).decode()
    def do_GET(self):
        self.send_response(200)
        self.send_header("Ignored-Header", "ignore me")
        self.send_header("Content-type", "text/html")
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(b'<form method="post"><textarea name="_"></textarea><input type="submit"></form>')
        return
    def do_POST(self):
        try: self.do_POST_handle()
        except:
            self.send_response(429)
            self.send_header("Connection", "close")
            self.end_headers()
        return

    @limits(calls=5, period=60)
    def do_POST_handle(self):
        if not (valid := self.headers.get("Authorization") == "Basic " + self._auth):
            self.send_response(401)
            self.send_header("WWW-Authenticate", f'Basic realm="{AUTHOR} Realm"')
            self.end_headers()
        #    return
        body_size = int(self.headers.get('content-length'))
        if body_size > MAX_SIZE_BODY:
            self.send_response(413)
            self.send_header("Connection", "close")
            self.end_headers()
            return
        post_body = momoryview(self.rfile.read(body_size))[2:]
        self.send_response(200)
        self.send_header("Content-type", 'application/octet-stream')
        self.send_header("Content-Disposition", f'attachment; filename="{AUTHOR}.txt"')
        self.send_header("Content-Encoding", "br")
        self.send_header("Connection", "close")
        self.end_headers()
        if valid:
            print(password := ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(32)))
            Server._auth = base64.b64encode(f"{AUTHOR}:{password}".encode()).decode()
            if not pattern.fullmatch(post_body):
                self.wfile.write(b'invalid format')
                return
            with open(AUTHOR, "wb") as inp: inp.write(post_body)
            try: out = subprocess.check_output(['your-command-that-print-to-stdout.exe', AUTHOR])
            except: out = post_body
            self.wfile.write(brotli.compress(out))
        return

test(Server, HTTPServer, port=8000)
