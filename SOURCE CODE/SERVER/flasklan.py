from flask import Flask, render_template, request, jsonify, redirect
from flask_bootstrap import Bootstrap
from mains import *
#import Queue



app = Flask(__name__)

Bootstrap(app)

ips=[]

@app.route('/')
def index():
     Thread(target = Main, args = ()).start()
     createFolders()
     return redirect("/monitor")

@app.route('/monitor')    
def monitor():  
    return render_template('index.html',var = ips, adds = addrs, col = colors, isStudent = isStudent)
   
@app.route('/try1')
def try1():
    emptyFolders()
    return redirect("/monitor")

@app.route('/', methods=['POST'])
def getvalue():
    msg=request.form['submit']
    return redirect("/monitor")

    
#gets ip for live ss of 1 pc
@app.route('/live', methods=['POST'])
def live():
    global clients,addrs,isStudent
    ipA=request.form['submit']
    if ipA in addrs:
        ind = addrs.index(ipA)
        if isStudent[ind]:
            reqSS(clients[ind])
    return redirect("/monitor")

#send keywords to all connected PCs
@app.route('/disconnect', methods=['POST'])
def disconnect():
    global clients,addrs,isStudent
    ipA=request.form['submit']
    if ipA in addrs:
        disconn(ipA)
    return redirect("/monitor")

#disconnects specific pc
@app.route('/keyword', methods=['POST'])
def keyword():
    global clients,addrs,isStudent,keyset
    string2 = request.form['key_words']
    sessionkey(string2)
    for c in clients:
        ind = clients.index(c)
        if isStudent[ind]:
            sendkeywords(c,string2)
    return redirect("/monitor")

#gets ip for switching off 1 pc
@app.route('/off1', methods=['POST'])
def off1():
    global clients,addrs,isStudent
    ipA=request.form['submit']
    if ipA in addrs:
        ind = addrs.index(ipA)
        if isStudent[ind]:
            shutdown(clients[ind])
    return redirect("/monitor")
        
#switchoff all pcs 
@app.route('/offall')
def offall():
    global clients,addrs,isStudent
    for c in clients:
        ind = clients.index(c)
        if isStudent[ind]:
            shutdown(c)
    return redirect("/monitor")
    
#gets the broadcast message from user and saves it in the variable msg
@app.route('/broadcast', methods=['POST'])
def broadcast():
    global clients,addrs,isStudent
    msg=request.form['b_msg']
    for c in clients:
        ind = clients.index(c)
        if isStudent[ind]:
            sendmessage(c,msg)    
    return redirect("/monitor")      
    
#gets ip and message for one pc   
@app.route('/message1', methods=['POST'])
def message1():
    global clients,addrs,isStudent
    IPa=request.form['get_ip']
    print(IPa)
    msg=request.form['message']
    if IPa in addrs:
        ind = addrs.index(IPa)
        if isStudent[ind]:
            sendmessage(clients[ind],msg)
            print('msg sent'+str(ind))
    return redirect("/monitor")

if __name__ == '__main__':
    
     app.run(debug=True)
     


    
