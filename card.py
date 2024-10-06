from http.server import BaseHTTPRequestHandler, HTTPServer, test
from socketserver import ThreadingMixIn
from http.cookies import SimpleCookie
import json
import requests
import datetime
import re
import redis

class Server(ThreadingMixIn, BaseHTTPRequestHandler):
    sess = requests.session()
    red_client = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
    @staticmethod
    def get_json(url, ignore_redis=False):
        if ignore_redis: return tor.get(url, Server.sess).json()
        is_redis = True
        try: Server.red_client.ping()
        except: is_redis = False
        data = None
        if is_redis:
            if not (data := Server.red_client.get(url)):
                data = tor.get(url, Server.sess).text
                Server.red_client.set(url, data)
            return json.loads(data)
        return tor.get(url, Server.sess).json()
    def send_header(self, keyword, value):
        if hasattr(self, 'response_text'): self.response_text += ("%s: %s\r\n" % (keyword, value))
        super().send_header(keyword, value)
    def end_headers(self):
        if hasattr(self, 'response_text'): self.response_text += "\r\n"
        super().end_headers()
    def write(self, s):
        if hasattr(self, 'response_text'): self.response_text += s
        self.wfile.write(s.encode('utf-8'))
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Headers", "X-Src")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        return
    def do_GET(self):
        if self.path == '/decks':
            data = Server.get_json("url-to-fetch")
            data = list(map(lambda z: {'name': z['name'], 'price': z['price'], 'id': z['id'], 'rarity': z['rarity'], 'setCode': z['setCode'], 'src': z['src'] }, data))
            for d in data:
                det = Server.get_json(f"url-to-fetch-detail")[0]
                d['hp'] = det.get('hp', 0)
                d['tcgplayer_id'] = det.get('tcgplayer_id', 0)
                d['supertype'] = det.get('supertype', 'Unknown')
                d['subtype'] = det.get('subtype', 'Unknown')
                d['type'] = det.get('type', 'Unknown')
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header('Content-Type', 'application/json')
            self.send_header('Connection', 'Close')
            self.end_headers()
            self.write(json.dumps(data))
            return
        if self.path == '/decks-yugi':
            data = Server.get_json("url-to-fetch")[0]
            data = list(map(lambda z: {'name': z['name'], 'price': float(z['price'])*12, 'id': z['id'], 'rarity': z['rarity'], 'setCode': z['setcode'], 'supertype': z['type'], 'src': z['image_url'], 'tcgplayer_id': re.search(r'product%2F(\d+)', z['card_url']).group(1) }, data))
            for d in data:
                if 'Monster' not in d['supertype']: continue
                det = Server.get_json(f'url-to-fetch-detail')['data'][0]
                d['hp'] = det.get('atk', 0)
                d['subtype'] = det.get('frameType', 'Unknown')
                d['type'] = det.get('attribute', 'Unknown')
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header('Content-Type', 'application/json')
            self.send_header('Connection', 'Close')
            self.end_headers()
            self.write(json.dumps(data))
            return
        if self.path == '/proxy':
            url = self.headers.get('X-Src')
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            r = Server.sess.get(url, stream=True)
            for k, v in r.headers.items(): self.send_header(k, v)
            self.send_header('Connection', 'Close')
            self.end_headers()
            #for chunk in r.iter_content(chunk_size=8192): self.wfile.write(chunk)
            self.wfile.write(r.raw.data)
            r.close()
            print(url)
            return
        
PORT = 8000
test(Server, HTTPServer, port=PORT)
