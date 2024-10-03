import socks
import socket
from stem.control import Controller
from stem import Signal
import cloudscraper
from fake_useragent import UserAgent
import time
import requests
import json

proxy_port = 9150
control_port = 9151 # socks5 port
tunnel_port = 9080 # http tunnel port 

# tor --hash-password "put your tor password here"
def renew_tor():
    with Controller.from_port(port = control_port) as controller:
        controller.authenticate(password="put your tor password here")
        controller.signal(Signal.NEWNYM)

def renew_session():
    scraper = cloudscraper.create_scraper()
    scraper.headers["User-Agent"] = str(UserAgent(os='linux', min_percentage=1.3).random)
    scraper.proxies = {'http': f'socks5://127.0.0.1:{proxy_port}', 'https': f'socks5://127.0.0.1:{proxy_port}'}
    #scraper.proxies = {'http': f'http://127.0.0.1:{tunnel_port}', 'https': f'http://127.0.0.1:{tunnel_port}'}
    return scraper

def a_new_me():
    print("Your Public IP:", requests.get("https://httpbin.org/ip").text, requests.get("https://icanhazip.com").text)
    #print("Your Public IP:", requests.get("https://icanhazip.com").text) #https://ident.me/
    renew_tor()
    sess = renew_session()
    print("IP rotated to:", sess.get("https://httpbin.org/ip").text, sess.get("https://icanhazip.com").text)
    #print("IP rotated to:", sess.get("https://icanhazip.com").text) #https://ident.me/
    return sess

def get(url, sess=None):
    if not sess: sess = a_new_me()
    r = sess.get(url)
    if r.status_code == 200: print(f"Done {url}"); return r
    if r.status_code == 403: return get(url)
    return f"Fail: Unknown code {r.status_code}"

def post(url, json={}, params={}, sess=None):
    if not sess: sess = a_new_me()
    r = sess.post(url, json=json, params=params,)
    if r.status_code == 200: print(f"Done {url}"); return r
    if r.status_code == 403: time.sleep(3); return post(url, json, params)
    return f"Fail: Unknown code {r.status_code}"
