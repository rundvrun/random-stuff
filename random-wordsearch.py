import requests, json, webbrowser, glob, random

cookies = {}

headers = {
    'accept': '*/*',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://thewordsearch.com',
    'pragma': 'no-cache',
    'referer': 'https://thewordsearch.com/maker/',
}
words = list(map(lambda s: s.replace('englishpic\\', '')[:-4], random.sample((l := [w for w in glob.glob('englishpic/*.jpg') if len(w) <= 30]), k=min(len(l), 30)))) # get random words ['an', 'apple', 'is', 'on', 'the', 'tree']
_json = {'id': -1, 'hash': '', 'ispersonal': 0, 'title': 'Your game title', 'desc': 'Your list description', 'wordlist': words}

print(_json["wordlist"])

data = {
    'json': json.dumps(_json, separators=(',',':')),
}

response = requests.post(
    'https://thewordsearch.com/api/pri/testapikey/save_word_search/',
    cookies=cookies,
    headers=headers,
    data=data,
)

id = json.loads(response.text)["result"]["id"]
url = f'https://thewordsearch.com/puzzle/{id}'
webbrowser.open(url, new=0, autoraise=True)
