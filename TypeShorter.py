import tkinter as tk
from tkinter import *
import os
from pynput.keyboard import Key, Controller,Listener
from PIL import Image,ImageTk
from os.path import exists
import subprocess
import threading

if(not(exists("Dictionary.txt"))):
    with open('Dictionary.txt', 'w',encoding='utf8') as file:
        file.writelines([
            "ko:không\n",
            "bth:bình thường\n",
            "cmt:comment\n",
            "avt:avatar\n",
            "stt:status\n",
            "g9:good night\n",
            "btw:by the way\n",
            "np:no problem\n"
        ])
    subprocess.check_call(["attrib","+H","Dictionary.txt"])

myKeyboard = Controller()
wordDetector = ""
def findWord(acronym):
	file = open('Dictionary.txt', 'r',encoding='utf8')
	lines = file.readlines()
	for line in lines:  
		dic = line.split(":")
		if (acronym.lower() == dic[0]):
			return dic[1]
	return "None"
def replaceWord(acronymLength,word):
	for i in range(0,acronymLength + 1):
		myKeyboard.press(Key.backspace)
		myKeyboard.release(Key.backspace)
	myKeyboard.type(word[0:len(word) - 1])
	myKeyboard.press(Key.space)
	myKeyboard.release(Key.space)
def on_press(key):
	if key == Key.f12:
		raise SystemExit(0)
	global wordDetector
	keyword = str(key).replace('\'',"")
	if (len(keyword) != 1 and key != Key.space and key != Key.shift):
		return
	if (key == Key.space):
		temp = findWord(wordDetector)
		if(temp != "None"):
			replaceWord(len(wordDetector),temp)
		wordDetector=""
		return
	wordDetector = wordDetector + keyword
	print(wordDetector)
def on_release(key):
	global wordDetector
	if (key == Key.backspace):
		wordDetector = wordDetector[0:len(wordDetector) - 1]
		print(wordDetector)
	if key == Key.f12:
		raise SystemExit(0)

def RunCore():
    with Listener(on_press=on_press,on_release=on_release) as listener:
	    listener.join()

try:
    t1 = threading.Thread(target=RunCore)
    t1.start()
except:
    print("Error: unable to start thread")

window=tk.Tk()
myKeyboard = Controller()
def on_closing():
    myKeyboard.press(Key.f12)   
    window.destroy()
def addWord(acronym,word):
    with open('Dictionary.txt', 'r+',encoding='utf-8') as file: 
        file_data = file.read()
        file.seek(0, 0)
        file.write(acronym.lower()+":"+word.lower()+'\n'+file_data)

def handleInput():
    acronymInput = acronym.get()
    wordInput = word.get()  
    if (acronymInput.strip() == "" or wordInput.strip() == ""):
        announce.config(text = "Bạn đang để trống input, hãy nhập lại!")
    else:
        addWord(acronymInput.strip(),wordInput.strip())
        getData()
        acronym.delete(0,END)
        word.delete(0,END)
        announce.config(text = "Thêm thành công")

def getData():
    file = open('Dictionary.txt', 'r',encoding='utf8')
    lines = file.readlines()
    count = 0
    data = "Một số ví dụ: \n"
    for line in lines:
        if (count == 10):
            break
        line = line[0:len(line) - 1]
        dic = line.split(":")
        data = data + dic[0] + "->" + dic[1]+"\n"
        count = count + 1
    words.config(text=data)

window.title("Type Shorter")
window.geometry("700x500")
window.resizable(0,0)
window.configure(bg='#F2D2BD')

tk.Label(window, text="Từ viết tắt",font=("Arial",12,'bold'),fg="#E70B64",bg="#FFFAA0").place(x=30,y=20)
acronym = tk.Entry(window,font=("Arial",20),bg="#F88379",fg="black",borderwidth = 4)
acronym.place(x=20,y=60)
tk.Label(window, text="Từ viết thường",font=("Arial",12,'bold'),fg="#E70B64",bg="#FFFAA0").place(x=30,y=110)
word = tk.Entry(window,font=("Arial",20),bg="#F88379",fg="black",borderwidth = 4)
word.place(x=20,y=150)
button = tk.Button(window, text="Thêm từ",font=("Arial",12,'bold'),bg="#FFFAA0",fg="#E70B64",borderwidth = 4,command=handleInput)
button.place(x=130,y=200)
announce = tk.Label(window,font=("Arial",12,'bold'),fg="#E70B64",bg='#F2D2BD')
announce.place(x=50,y=250)

words = tk.Label(window,font=("Arial",12,'bold'),fg="#E70B64",bg='#F2D2BD')
words.place(x=50,y=280)

tk.Label(window, text="Bạn có thể thêm 1 từ viết tắt\n và nghĩa viết thường",font=("Arial",12,'bold'),fg="#E70B64",bg="#FFFAA0").place(x=400,y=40)
tk.Label(window, text="Nhấn nút thêm vào trả nghiệm nào <3",font=("Arial",12,'bold'),fg="#E70B64",bg="#FFFAA0").place(x=400,y=100)

if(exists("TMT_REY.png")):
    TmtRey = Image.open("TMT_REY.png")
    resized_image= TmtRey.resize((250,233), Image.Resampling.LANCZOS)
    TmtRey = ImageTk.PhotoImage(resized_image)
    tk.Label(window,bg="#F2D2BD",image=TmtRey).place(x=380,y=180)
getData()

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
