import aiohttp        
import aiofiles
import asyncio
import os
import json
from pathlib import Path
import requests
import re
from datetime import datetime

file_postfix = datetime.now().strftime("%Y%m%d%H%M%S")
json_numbers = Path('fbid.json').read_text()
numbers = json.loads(json_numbers)

cookies_path = Path('../cookies.json').read_text()
cookies = json.loads(cookies_path)
print(cookies)

cookies = {
    'datr': 'iDSdY2sFg26yH4KS5Ruf1v7v',
    'wd': '1215x1013',
}

headers = {
    'authority': 'www.facebook.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}

limit_sub = 300
total = len(numbers)
url = "https://www.facebook.com/photo.php"

_t = asyncio.create_task

async def write_json(data, filename):
    async with aiofiles.open(filename, mode='w') as fpw:
        await fpw.write(json.dumps(data, indent=6))
        
async def download_file(url, filepath):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp_download:
            if resp_download.status == 200:   
                async with aiofiles.open(filepath, mode='wb') as fpd:
                    await fpd.write(await resp_download.read())
                    print(f'{url} -> {filepath} done')

async def main():
    global url, total, limit_sub, file_postfix, headers, cookies
    
    async with aiohttp.ClientSession(headers=headers, cookies=cookies) as session:
        urls = []
        urls_json = []
        i = 0
        chapter = 0
        
        for num in numbers:
            params = {
                'fbid': num,
                'set': 'pb.100070717965590.-2207520000.',
                'type': '3',
            }
            async with session.get(url, params=params) as resp:
                if resp.status == 200:
                    #print(await resp.text())
                    #print(resp.content)
                    #print(dir(resp))
                    t = str(await resp.content.read())
                else:
                    t = ''
            print(f'\n{num}:')
            if t == '':
                break
            if i % limit_sub == 0:
                while True:
                    chapter += 1
                    dir_path = f'pictures\\chapter{chapter}'
                    os.system(f'mkdir {dir_path}')
                    count_file = len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))])
                    print(f'{dir_path}: {count_file} files')
                    if count_file < limit_sub:
                        i = count_file
                        break
            i += 1

            _urls_ = list(filter(lambda xx: xx.find('_nc_cat=') >= 0 and xx.find('p40x40') < 0 and xx.find('dst-png_') < 0 and xx.find('dst-webp_') < 0 and xx.find('dst-jpg_') < 0 and xx.find('110x80') < 0, re.findall(r'href=[\'"]?([^\'" >]+)', t)))
            urls_ = list(set(map(lambda xx: xx.replace('amp;', ''), _urls_)))
            print(urls_)
            
            urls_json.append({num: urls_, chapter: chapter})
            task_write_main = _t(write_json(urls_json, f'urls_json_{file_postfix}.json'))
            
            for urlx in urls_:
                print(f'{urlx}')
                file_name = re.search(r"\d+_\d+_\d+_[no]\.(png|jpg|jpegW|webp)", urlx).group()
                print(file_name)
                urls.append(urlx)
                task_write_detail = _t(write_json(urls, f'urls_{file_postfix}.json'))
                
                dir_down = f'pictures\\chapter{chapter}\\{file_name}'
                print(dir_down)
                    
                task_download = _t(download_file(urlx, dir_down))
                
                await asyncio.gather(task_write_main, task_write_detail, task_download)
            
            if urls_ == []:
                print(num)
                await task_write_main
                break

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
