import requests
import json
import random

import time

with open('random_small_conv.json', 'r', encoding="utf-8") as f:
    data = json.load(f)
    print(len(data))

with open('oxford3000.txt', 'r', encoding="utf-8") as f:
    words = f.readlines()
    print(len(words))

headers_q = {
    'Authorization': 'Bearer <LINE bot access token>',
    'Content-Type': 'application/x-www-form-urlencoded',
}

headers_a = {
    'Authorization': 'Bearer <LINE bot access token>',
    'Content-Type': 'application/x-www-form-urlencoded',
}

def A(m):
    msg = {
        'message': m,
    }
    return requests.post('https://notify-api.line.me/api/notify', headers=headers_a, data=msg)

def Q(m):
    msg = {
        'message': m,
    }
    return requests.post('https://notify-api.line.me/api/notify', headers=headers_q, data=msg)

def random_conv():
    global data
    qa_pair = random.choice(data)
    data.remove(qa_pair)
    Q(f"{qa_pair['question']}")
    A(f"{qa_pair['answer']}")
    Q("========Conv==========")

def get_word(word):
    json_w = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}').json()
    return simplify_word(json_w)

def simplify_word(json_word):
    if type(json_word) is dict:
        return None
    res = []
    for entry in json_word:
        word = entry["word"]
        phonetics_text = [phonetic["text"] for phonetic in entry["phonetics"] if 'text' in phonetic]
        meanings_definitions = []
        for meaning in entry["meanings"]:
            definitions = [{ 'def': definition["definition"], 'ex': definition["example"] if "example" in definition else '' } for definition in meaning["definitions"]]
            #definitions = [definition["definition"] for definition in meaning["definitions"]]
            #examples = [example["example"] for example in meaning["definitions"] if "example" in example]
            meanings_definitions.append({"part_of_speech": meaning["partOfSpeech"], "definitions": definitions})
        result = {"word": word, "phonetics": phonetics_text, "meanings": meanings_definitions}
        res.append(result)
    return res

def print_word(word):
    word_def = get_word(word)
    if word_def is None:
        return None
    w = word_def[0]['word']
    for wd in word_def:
        ipa = str.join('||', wd['phonetics'])
        Q(f'Word: {w} ({ipa})')
        meanings = wd['meanings']
        for meaning in meanings:
            t = meaning['part_of_speech']
            defn = meaning['definitions']
            for d in defn:
                A(f"Def ({t}): {d['def']}")
                ex = d['ex']
                if ex != '':
                    A(f"Ex: {ex}")
    Q("========Word==========")
    return word_def

def random_word():
    global words
    word = random.choice(words)
    words.remove(word)
    try:
        word_def = print_word(word)
    except:
        word_def = None
    if word_def is None:
        return random_word()
    
    return True

while True and len(data) > 0:
    random_word()
    time.sleep(360)
    random_conv()
    time.sleep(480)
