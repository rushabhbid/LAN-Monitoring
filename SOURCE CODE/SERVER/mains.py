from threading import Thread, Lock
import socket
import os
import time
import shutil

clients = []
addrs = []
isStudent = []
keyset = "`~"
colors = ["Aqua","Aqua","Aqua","Aqua","Aqua","Aqua","Aqua","Aqua","Aqua","Aqua","Aqua","Aqua","Aqua","Aqua","Aqua","Aqua","Aqua","Aqua","Aqua","Aqua"]
lock = Lock()
flag = 0

def createFolders():
    for i in range(20):
        clientfolder = "static/img/comp"+str(i+1)
        if not os.path.exists(clientfolder):
            os.makedirs(clientfolder)
        static_img = "static/img/comp"+str(i+1)+"/0.png"
        if os.path.exists(static_img):
            onlyfiles = len(next(os.walk(clientfolder))[2])
            new_img = "static/img/comp"+str(i+1)+"/"+str(onlyfiles)+".png"
            os.rename(static_img,new_img)
        shutil.copyfile("static/blank.png",static_img)

def emptyFolders():
    global flag
    
    while flag==1:
        time.sleep(0.2)
    
    flag = 1
    
    for i in range(20):
        clientfolder = "static/img/comp"+str(i+1)
        for file in os.listdir(clientfolder):
            file_path = os.path.join(clientfolder, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        static_img = clientfolder+"/0.png"
        shutil.copyfile("static/blank.png",static_img)
    flag = 0

def acceptClients(s):
    global clients,isStudent,keyset
    global addrs
    while True:
        ind = -1
        c, addr = s.accept()
        addr = str(addr)
        only_ip = addr.split(',')
        for add in addrs:
            compare_ip = add.split(',')
            if compare_ip[0] == only_ip[0]:
                ind = addrs.index(add)
                break
        
        if ind != -1:
            clients[ind] = c
            addrs[ind] = addr
            isStudent[ind] = True
        
        else:
            clients.append(c)
            addrs.append(addr)
            isStudent.append(True)
            
        print("Client IP: <"+ addr+"> connected successfully !!");
        sendkeywords(c, keyset)

def sessionkey(string):
    global keyset
    keyset = string	

def reqSS(c):
    global clients,addrs,colors,flag
    
    while flag==1:
        time.sleep(0.2)
    
    flag = 1
    
    try:
        c.send(str.encode("BHEJO"))
        print(1)
        data = c.recv(1024)
        datastr = data.decode("UTF-8")
        if datastr[:6] == "EXISTS":
            filesize = int(datastr[6:])
            print(filesize)
            message = 'Y'  #input("File exists, " + str(filesize) + "Bytes, download? (Y/N)? -> ")
            if message == 'Y':
                c.send(str.encode("OK"))
                
                clientfolder = "static/img/comp"+str(clients.index(c)+1)
                static_img = "static/img/comp"+str(clients.index(c)+1)+"/0.png"
                onlyfiles = len(next(os.walk(clientfolder))[2])
                new_img = "static/img/comp"+str(clients.index(c)+1)+"/"+str(onlyfiles)+".png"
                newfile = "static/img/comp"+str(clients.index(c)+1)+"/temp.png"
                
                f = open(newfile, 'wb')
                data = c.recv(1024)
                totalRecv = len(data)
                f.write(data)
                while totalRecv < filesize:
                    data = c.recv(1024)
                    totalRecv += len(data)
                    f.write(data)
                    print("{0:.2f}".format((totalRecv / float(filesize)) * 100) + "% Done")
                f.close()
                print("Download Complete!")
                
                print(onlyfiles)
                
                os.rename(static_img,new_img)
                os.rename(newfile,static_img)
                
    
        else:
            print("File Does Not Exist!")
            
    except:
        print('sock error')                
    
    flag = 0


def sendmessage(c,msg):
    try:
        global clients,addrs,colors,flag
        
        while flag==1:
            time.sleep(0.2)
        
        flag = 1
        c.send(str.encode("MESSAGE"))
        ack = c.recv(1024)
        if ack == b"OK":
            c.send(str.encode(str(msg)))
            print('on the way')
        flag = 0
    
    except:
        print("sock error")
        
def disconn(addr):
    global clients,addrs,colors,flag,isStudent
        
    while flag==1:
        time.sleep(0.2)
        
    flag = 1
        
    if addr in addrs:
        ind = addrs.index(addr)
        if isStudent[ind]:
            isStudent[ind] = False
            clientfolder = "static/img/comp"+str(ind+1)
            static_img = "static/img/comp"+str(ind+1)+"/0.png"
            if os.path.exists(static_img):
                onlyfiles = len(next(os.walk(clientfolder))[2])
                new_img = "static/img/comp"+str(ind+1)+"/"+str(onlyfiles)+".png"
                os.rename(static_img,new_img)
            shutil.copyfile("static/blank.png",static_img)
        else:
            isStudent[ind] = True

    flag = 0

def shutdown(c):
    try:
        global clients,addrs,colors,flag
        
        while flag==1:
            time.sleep(0.2)
        
        flag = 1
        c.send(str.encode("SHUTDOWN"))
        flag = 0
        
    except:
        print("sock error")

def sendkeywords(c,string2):
    try:
        global clients,addrs,colors,flag
		
        while flag==1:
            time.sleep(0.2)
        
        flag = 1
        c.send(str.encode("KEYWORDS"))
        ack = c.recv(1024)
        if ack == b"OK":
            c.send(str.encode(str(string2)))
            print('on the way')
        flag = 0
    
    except:
        print("sock error")
    
def Main():
    
    global clients,isStudent
    global addrs
    
    str = open('server_ip.txt', 'r').read()
    print(str)
    
    host = str
    port = 2224
    
    try:    
        s = socket.socket()
        s.bind((host,port))
        
        s.listen(5)
        
        print("Server Started!!")
        
        Thread(target = acceptClients, args = (s,)).start()
        while True:    
            print(clients)
            print(addrs)
            for c in clients:
                ind = clients.index(c)
                if isStudent[ind]:
                    reqSS(c)
                    time.sleep(1)
            time.sleep(10)
            
    except:
        print("Some jhol")
    finally:
        s.close()
