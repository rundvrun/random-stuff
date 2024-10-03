from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import os
import aiohttp        
import aiofiles
import asyncio
import json
from pathlib import Path

def open(url):
    chromedriver_path = r'F:\chromedriver_win32\chromedriver.exe'
    brave_path = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'

    s = Service(chromedriver_path)

    option = webdriver.ChromeOptions()
    option.binary_location = brave_path
    option.add_argument("--incognito")
    option.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=s, options=option)
    driver.get(url)
    time.sleep(5)
    cookies_list = driver.get_cookies()

#print(cookies_list)
    o = dict()
    for c in cookies_list:
        n = c['name']
        v = c['value']
        if n == '_js_datr':
            n = 'datr'
        o[n] = v
    driver.close()
    return o

async def write_json(data, filename):
    async with aiofiles.open(filename, mode='w') as fpw:
        await fpw.write(json.dumps(data, indent=6))

cookies = open('https://www.facebook.com/photo.php?fbid=217195370647727&set=pb.100070717965590.-2207520000.&type=3')
print(cookies)
os.system(f'echo cookies = {cookies} | clip')

async def main():
    global cookies
    await write_json(cookies, 'cookies.json')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
