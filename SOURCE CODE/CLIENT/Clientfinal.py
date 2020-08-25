# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 23:39:40 2018

@author: Rushabh
"""

from PIL import Image,ImageOps
import pytesseract
import cv2
import socket
from threading import Thread
import time
import os
import pyautogui
import subprocess
import ctypes  # An included library with Python install.
    
message = "null"
str2 = ""

def shutdown():
    subprocess.call(["shutdown", "-f", "-s", "-t", "1"])

def RetrFile(name,sock):

        global str2
        pyautogui.screenshot('demo.png')
        
        image = cv2.imread('demo.png')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 0, 255,
        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        filename = "{}.png".format(os.getpid())
        cv2.imwrite(filename, gray)
        text = pytesseract.image_to_string(Image.open(filename))
        os.remove(filename)
        import re
        words = re.split(r'\W+', text)
        
        str1=[x.lower() for x in words]
        print(str1)
        
        a = str2.split(",")
        str12 = [x.lower() for x in a]
        print(str12)
        
        count = 0
        for num in str1:
            if num in str12:
               count=count+1
        
        if count < 1:
            color = 'red'
            ImageOps.expand(Image.open('demo.png'),border=50,fill='red').save('demo.png')
        elif count >= 1 and count < 2:
            color = 'yellow'
            ImageOps.expand(Image.open('demo.png'),border=50,fill='yellow').save('demo.png')
        else:
            color = 'green'
            ImageOps.expand(Image.open('demo.png'),border=50,fill='green').save('demo.png')
            
        print("color")
        print(color)
        
        filename = 'demo.png'
        
        if os.path.isfile(filename):
            print(filename)
            binostr = "EXISTS"+str(os.path.getsize(filename))
            bino = str.encode(binostr)
            sock.send(bino)
            filesize = int(binostr[6:])
            #filesize = int.from_bytes(binostr[6:], byteorder = 'big', signed = True)
            print(filesize)
            userResponse = sock.recv(1024)
            print(userResponse)
            if userResponse[:2] == b'OK':
                with open(filename, 'rb') as f:
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
                    while bytesToSend :
                        bytesToSend = f.read(1024)
                        sock.send(bytesToSend)
            print(1)
            
        else:
            sock.send("ERR ")
            print('no file')
        
        
        f = open("myfile.txt", "w")
        with open("myfile.txt" , "w", encoding="utf-8") as f:
            f.write(str(words))

            
        return
        
def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, "Message From ADMIN", style)
        
def viewmessage(s):
    s.send(str.encode("OK"))
    msg = s.recv(1024)
    message = msg.decode("UTF-8")
    t = Thread(target = Mbox, args = ('Message From ADMIN', message, 0,))
    t.daemon = True
    t.start()
    

def setkeywords(s):
    global str2
    s.send(str.encode("OK"))
    string2 = s.recv(1024)
    str2 = string2.decode("UTF-8")
    print(str2)

def sendInvoke(s):
    while True:
        command = s.recv(1024)
        if command == b"BHEJO":
            RetrFile("RetrThread",s)
            print(1)
            command = b"Mat BHEJO THODI DER"
            print(command)
            
        elif command == b"SHUTDOWN":
            shutdown()
            
        elif command == b"MESSAGE":
            print("Message")
            viewmessage(s)

        elif command == b"KEYWORDS":
            print("Keywords")
            setkeywords(s)

def Main():
    
    str = open('server_ip.txt', 'r').read()
    host = str
    port = 2224
    
    s = socket.socket()
    
    while True:
        try:
            s.connect((host,port))
            break
        except socket.error as e:
            print(str(e))
            time.sleep(10)
    
    sendInvoke(s)
    
    s.close()
    
if __name__ == '__main__':
    Main()
