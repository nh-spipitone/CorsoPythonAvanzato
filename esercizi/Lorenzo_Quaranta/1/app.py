from flask import Flask, render_template, request, redirect,url_for,flash
import json
from os import path,mkdir
from itertools import count
app = Flask(__name__)
id_iterator=count(0,1)
if(not path.exists("data/messages.json") ):
    if not path.exists("data"):
        mkdir("data")
    messaggi=open("./data/messages.json","x")
    json.dump([],messaggi)
    messaggi.close()

    

@app.route("/")
def home():
    messaggi_json =open("data/messages.json","r")
    messaggi=json.load(messaggi_json)
    print(messaggi)
    messaggi_json.close()
    return render_template("home.html",messaggi=messaggi)

@app.route("/new",methods=["GET", "POST"])
def newmsg():
    if(request.method=="POST"):
        author=request.form['author']
        text=request.form['text']
        newmessage={"author":author,"text":text}
        messaggi=open("data/messages.json","r")
        mess_lista=json.load(messaggi)
        newmessage['id']=next(id_iterator)
        mess_lista.append(newmessage)
        messaggi.close()
        messaggi=open("data/messages.json","w")
        json.dump(mess_lista,messaggi)
        messaggi.close()
        return redirect(url_for("home"))
    else:
        return render_template("new.html")
    
@app.route("/msg/<int:msg_id>")
def search(msg_id):
    messaggi=open("data/messages.json","r")
    mess_lista=json.load(messaggi)
    messaggio=[mess for mess in mess_lista if mess['id']==msg_id]
    messaggio= messaggio[0] if messaggio else None
    messaggi.close()
    if messaggio==None:
        return render_template("404.html")
    else: return render_template("show",messaggio=messaggio)


    
if __name__=="__main__":
    app.run(debug=True)