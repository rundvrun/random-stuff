import win32com.client, win32con #, autopy
shell = win32com.client.Dispatch("WScript.Shell")
wnd = "GamezBD - 405306"
active = lambda name: shell.AppActivate(name)
import time
import win32api, win32con
import ctypes
import re
import datetime
import asyncio
from playsound import playsound
#import clr
#clr.AddReference("System.Windows.Forms")
#from System.Windows.Forms import MessageBox
import keyboard
t = True
def T():
	global t
	t = False
keyboard.add_hotkey('ctrl+shift',  T)
with open('dik.h') as dik_f:
	lines = dik_f.readlines()
fnc = lambda s: re.match(r'#define ((DIK|DIKEYBOARD)_\w+)\s+(0x*.{2,4})', s).groups()
code = list(map(fnc, lines))
code = {k:int(v, 0) for (k, _, v) in code}
#locals().update(code) # for variables
from types import SimpleNamespace   
sc = SimpleNamespace(**code) # for namespace variables
#needle = autopy.bitmap.Bitmap.open('flag.png')
# win32api.MapVirtualKey
from gtts import gTTS
txt = "Xong "# * 5
fname = f"R:\play.mp3"
myobj = gTTS(text=txt, lang='vi', slow=False)
import os
if not os.path.isfile(fname):
    myobj.save(fname)
SendInput = ctypes.windll.user32.SendInput

PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]
def check_stop():
	return autopy.bitmap.capture_screen(  ).find_bitmap(needle) != None
class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

cache_p = dict()

import mouse
def mouseXUP(m):
    if type(m) is mouse.ButtonEvent:
        if m.button == mouse.X and m.event_type == 'up':
            autoFarm()
mouse.hook(mouseXUP)

def mouseXUP1(m):
    if type(m) is mouse.ButtonEvent:
        if m.button == mouse.X and m.event_type == 'up':
            autoGuard()

#mouse.hook(mouseXUP1)

def autoGuard():
    active(wnd)
    pydirectinput.press('2')
    time.sleep(3)
    pydirectinput.press('3')
    time.sleep(3)
    pydirectinput.press('1')

def autoSQ():
    #keyboard.press_and_release('w+c')
    #time.sleep(1)
    keyboard.press_and_release('shift+s+q')

#mouse.on_button(autoGuard, args=(), buttons=('x'), types=('up'))
#mouse.on_button(autoSQ, args=(), buttons=('x'), types=('up'))

def PressKey(hexKeyCode):
    if True or hexKeyCode not in cache_p:
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
        x = Input( ctypes.c_ulong(1), ii_ )
        #cache_p[hexKeyCode] = x
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

cache_r = dict()

def ReleaseKey(hexKeyCode):
    if True or hexKeyCode not in cache_p:
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
        x = Input( ctypes.c_ulong(1), ii_ )
        #cache_r[hexKeyCode] = x
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def KeyPress():
    active(wnd)
    time.sleep(1.5)
    PressKey(0x10) # press Q
    time.sleep(.3)
    ReleaseKey(0x10) #release Q


VK_CODE = {'backspace':0x08,
           'tab':0x09,
           'clear':0x0C,
           'enter':0x0D,
           'shift':0x10,
           'ctrl':0x11,
           'alt':0x12,
           'pause':0x13,
           'caps_lock':0x14,
           'esc':0x1B,
           'spacebar':0x20,
           'page_up':0x21,
           'page_down':0x22,
           'end':0x23,
           'home':0x24,
           'left_arrow':0x25,
           'up_arrow':0x26,
           'right_arrow':0x27,
           'down_arrow':0x28,
           'select':0x29,
           'print':0x2A,
           'execute':0x2B,
           'print_screen':0x2C,
           'ins':0x2D,
           'del':0x2E,
           'help':0x2F,
           '0':0x30,
           '1':0x31,
           '2':0x32,
           '3':0x33,
           '4':0x34,
           '5':0x35,
           '6':0x36,
           '7':0x37,
           '8':0x38,
           '9':0x39,
           'a':0x41,
           'b':0x42,
           'c':0x43,
           'd':0x44,
           'e':0x45,
           'f':0x46,
           'g':0x47,
           'h':0x48,
           'i':0x49,
           'j':0x4A,
           'k':0x4B,
           'l':0x4C,
           'm':0x4D,
           'n':0x4E,
           'o':0x4F,
           'p':0x50,
           'q':0x51,
           'r':0x52,
           's':0x53,
           't':0x54,
           'u':0x55,
           'v':0x56,
           'w':0x57,
           'x':0x58,
           'y':0x59,
           'z':0x5A,
           'numpad_0':0x60,
           'numpad_1':0x61,
           'numpad_2':0x62,
           'numpad_3':0x63,
           'numpad_4':0x64,
           'numpad_5':0x65,
           'numpad_6':0x66,
           'numpad_7':0x67,
           'numpad_8':0x68,
           'numpad_9':0x69,
           'multiply_key':0x6A,
           'add_key':0x6B,
           'separator_key':0x6C,
           'subtract_key':0x6D,
           'decimal_key':0x6E,
           'divide_key':0x6F,
           'F1':0x70,
           'F2':0x71,
           'F3':0x72,
           'F4':0x73,
           'F5':0x74,
           'F6':0x75,
           'F7':0x76,
           'F8':0x77,
           'F9':0x78,
           'F10':0x79,
           'F11':0x7A,
           'F12':0x7B,
           'F13':0x7C,
           'F14':0x7D,
           'F15':0x7E,
           'F16':0x7F,
           'F17':0x80,
           'F18':0x81,
           'F19':0x82,
           'F20':0x83,
           'F21':0x84,
           'F22':0x85,
           'F23':0x86,
           'F24':0x87,
           'num_lock':0x90,
           'scroll_lock':0x91,
           'left_shift':0xA0,
           'right_shift ':0xA1,
           'left_control':0xA2,
           'right_control':0xA3,
           'left_menu':0xA4,
           'right_menu':0xA5,
           'browser_back':0xA6,
           'browser_forward':0xA7,
           'browser_refresh':0xA8,
           'browser_stop':0xA9,
           'browser_search':0xAA,
           'browser_favorites':0xAB,
           'browser_start_and_home':0xAC,
           'volume_mute':0xAD,
           'volume_Down':0xAE,
           'volume_up':0xAF,
           'next_track':0xB0,
           'previous_track':0xB1,
           'stop_media':0xB2,
           'play/pause_media':0xB3,
           'start_mail':0xB4,
           'select_media':0xB5,
           'start_application_1':0xB6,
           'start_application_2':0xB7,
           'attn_key':0xF6,
           'crsel_key':0xF7,
           'exsel_key':0xF8,
           'play_key':0xFA,
           'zoom_key':0xFB,
           'clear_key':0xFE,
           '+':0xBB,
           ',':0xBC,
           '-':0xBD,
           '.':0xBE,
           '/':0xBF,
           '`':0xC0,
           ';':0xBA,
           '[':0xDB,
           '\\':0xDC,
           ']':0xDD,
           "'":0xDE,
           '`':0xC0}
keys = VK_CODE

def keyPress(k):
    active(wnd)
    time.sleep(.2)
    PressKey(k) # press Q
    time.sleep(.05)
    ReleaseKey(k) #release Q

def capital(k):
	if k in 'abcdefghijklmnopqrstuvwxyz':
		code = keys[k]
		code += 0x20
	return code

def press(code):
	win32api.keybd_event(code, 0, 0, 0)
	time.sleep(.05)
	win32api.keybd_event(code, 0, win32con.KEYEVENTF_KEYUP, 0)

def clickL(x,y):
    #win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
def clickR(x,y):
    #win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)
def clickR_bdo(x, y):
	active(wnd)
	time.sleep(0.05)
	clickR(x, y)
def clickL_bdo(x, y):
	active(wnd)
	time.sleep(0.05)
	clickL(x, y)
def press_bdo(key):
	active(wnd)
	time.sleep(.05)
	win32api.keybd_event(key, 0, 2, 0)
	time.sleep(.05)
	win32api.keybd_event(key, 0, 0, 0)
d = 400
def doubleL_bdo(x, y):
	for i in range(3):
		clickL_bdo(x, y)
def doubleR_bdo(x, y):
	for i in range(3):
		clickR_bdo(x, y)
run_mouse = True and False
if run_mouse:
	for i in range(100):
		#click_bdo(960 - d if i % 50 > 24 else 960 + d, 550)
		print(i)
		for t in range(4):
			doubleL_bdo(1000, 540)
			time.sleep(1.8)
		time.sleep(32)
		for t in range(4):
			doubleR_bdo(1000, 540)
			time.sleep(1.8)
		time.sleep(32)
import datetime
def auto_gamez(minutes=10):
	end = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
	while datetime.datetime.now() <= end: 
		clickL_bdo(1000, 520);
		time.sleep(.1); 
		clickR_bdo(1000, 520)

def auto_gamez_rot():
	while True: #not check_stop(): 
		clickL_bdo(1000, 520);
		time.sleep(1);
		move_(5, 0)

def move_(dx, dy):
	nx = dx*65535/win32api.GetSystemMetrics(0)
	ny = dy*65535/win32api.GetSystemMetrics(1)
	win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(nx), int(ny))
    

import tkinter.messagebox
msgbox = tkinter.messagebox.Message()
def autoKey(keyCode=0x1C, duration=60):
    global t
    t = True
    endTime = datetime.datetime.now() + datetime.timedelta(seconds=duration)
    i = 0
    while datetime.datetime.now() < endTime and t:
        keyPress(keyCode)
    #playsound(fname)
    #MessageBox.Show("Xong")
    msgbox.show()

def keyPressF(k):
    active(wnd)
    time.sleep(.18)
    PressKey(k) # press Q
    time.sleep(.59)
    ReleaseKey(k) #release Q

def autoMilk(duration=9):
    keyPress(0x13)
    time.sleep(1.5)
    endTime = datetime.datetime.now() + datetime.timedelta(seconds=duration)
    while datetime.datetime.now() < endTime:
        keyPressF(0x10)
        keyPressF(0x12)
keyboard.add_hotkey("f10", autoMilk)
#mouse.on_button(autoMilk, args=(), buttons=('x2'), types=('up'))
def scrollMilk(m):
    if isinstance(m, mouse.WheelEvent) and m.delta == 1.0:
        autoMilk()
#mouse.hook(scrollMilk)

def autoR(duration=45):
    endTime = datetime.datetime.now() + datetime.timedelta(seconds=duration)
    active(wnd)
    while datetime.datetime.now() < endTime:
        #keyPress(0x13)
        pydirectinput.press('r')
        time.sleep(.3)
    #playsound(fname)
keyboard.add_hotkey("f9", autoR)

def autoSpace(duration=2000):
    endTime = datetime.datetime.now() + datetime.timedelta(seconds=duration)
    active(wnd)
    while datetime.datetime.now() < endTime:
        #keyPress(0x13)
        pydirectinput.press('space')
        time.sleep(1)

def autoE(duration=2000):
    endTime = datetime.datetime.now() + datetime.timedelta(seconds=duration)
    active(wnd)
    while datetime.datetime.now() < endTime:
        #keyPress(0x13)
        pydirectinput.press('e')
        time.sleep(1)

import os
def dis():
    os.system("taskkill /F /im python.exe")
keyboard.add_hotkey("f8", dis)

import tkinter as tk
from tkinter import simpledialog as askBox

#ROOT = tk.Tk()

#ROOT.withdraw()

def startCooking():
    print('how minute ')
    autoKey(0x1c, int(input("how minute ")) * 60)

#keyboard.add_hotkey("ctrl+enter", startCooking)

import pydirectinput
def autoFarm(n=10):
    active(wnd)
    x = 750
    y = 370
    for ix in range(2):
        for iy in range(n//2):
            #pydirectinput.moveTo(x, y)
            time.sleep(.18)
            pydirectinput.press('1')
            time.sleep(.18)
            pydirectinput.click()
            time.sleep(.18)
            pydirectinput.press('space')
            y += 100
        x += 100

def autoFarmR(n=20):
    active(wnd)
    for i in range(n):
        pydirectinput.press('r')
        time.sleep(3)

def autoF12(n=20):
    active(wnd)
    pydirectinput.keyDown('f12')

#keyboard.add_hotkey("enter+shift", autoFarm)

def autoGrind():
    active(wnd);
    pydirectinput.keyDown('w'); 
    pydirectinput.keyDown('q');
        
#keyboard.add_hotkey("enter+shift", autoGrind)

def click(n=10):
    active(wnd)
    for i in range(n):
        pydirectinput.click()
        time.sleep(.2)

def rightclick(n=10):
    active(wnd)
    for i in range(n):
        pydirectinput.rightClick()
        time.sleep(.2)

def gwitch():
    active(wnd)
    pydirectinput.keyDown('w'); 
    pydirectinput.keyDown('f12');

def startF5():
    print('how minute ')
    autoKey(0x3f, int(input("how minute ")) * 60)

def macrovalk():
    active(wnd)
    pydirectinput.mouseDown(button='right');
    #pydirectinput.keyDown('space');

#keyboard.add_hotkey('x', macrovalk)

def startSpace():
    print('how minute ')
    autoKey(0x39, int(input("how minute ")) * 60)