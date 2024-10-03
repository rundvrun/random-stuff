import requests
from requests.structures import CaseInsensitiveDict
from pyquery import PyQuery
import random
#from win10toast import ToastNotifier
import time
import tkinter, win32api, win32con, pywintypes
import pyttsx3
import threading

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('volume',1.0)
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 120)

def speak(m):
    engine.say(m)
    engine.runAndWait()
    engine.stop()

def toScreen(m):
    label = tkinter.Label(text=m, font=('Times New Roman','20'), fg='coral1', bg='black', wraplength=900)
    label.master.overrideredirect(True)
    label.master.geometry("+500+300")
    label.master.lift()
    label.master.wm_attributes("-topmost", True)
    label.master.wm_attributes("-disabled", True)
    label.master.wm_attributes("-transparentcolor", "white")

    hWindow = pywintypes.HANDLE(int(label.master.frame(), 16))
    # http://msdn.microsoft.com/en-us/library/windows/desktop/ff700543(v=vs.85).aspx
    # The WS_EX_TRANSPARENT flag makes events (like mouse clicks) fall through the window.
    exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST |     win32con.WS_EX_TRANSPARENT
    win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)
    return label

headers_q = {
    'Authorization': 'Bearer <your LINE bot token>',
    'Content-Type': 'application/x-www-form-urlencoded',
}

headers_a = {
    'Authorization': 'Bearer <your LINE bot token>',
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

#toaster = ToastNotifier()

url = "https://www.coolgenerator.com/sentence-generator"

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/x-www-form-urlencoded"

word = 'genuine' # test word
cnt = 2000

data = f"lang=0&contain={word}&quantity={cnt}"

resp = requests.post(url, headers=headers, data=data)

#print(resp.status_code)

parsed_html = PyQuery(resp.text)

ls = parsed_html('div.content ul li.col-sm-12 p.font-18')

sentences = list(map(lambda h: h.text_content(), ls))
print(len(sentences))
if sentences:
    #toaster.show_toast("", random.choice(sentences), duration=45)
    mess = random.choice(sentences)
    apprWord = 1 + mess.count(' ')
    root = tkinter.Tk()
    lbl = toScreen(mess.replace(word, f'*{word}*'))
    lbl.pack()
    threading.Thread(target=speak, args=(mess,)).start()
    root.after(5000 + 700 * apprWord, root.destroy)
    root.mainloop()
