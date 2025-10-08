from flask import Flask, render_template, request, redirect,url_for,flash
import json
from os import path,mkdir

def next_id(arr):
    return (arr[-1]["id"] + 1) if arr else 1

app = Flask(__name__)
if(not path.exists("data/messages.json") ):
    if not path.exists("data"):
        mkdir("data")
    messaggi=open("./data/messages.json","x", encoding="utf-8")
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
        messaggi=open("data/messages.json","r", encoding="utf-8")
        mess_lista=json.load(messaggi)
        newmessage['id']=next_id(mess_lista)
        mess_lista.append(newmessage)
        messaggi.close()
        messaggi=open("data/messages.json","w", encoding="utf-8")
        json.dump(mess_lista,messaggi)
        messaggi.close()
        return redirect(url_for("home"))
    else:
        return render_template("new.html")
    
@app.route("/msg/<int:msg_id>")
def show(msg_id):
    messaggi=open("data/messages.json","r")
    mess_lista=json.load(messaggi)
    messaggio=next((mess for mess in mess_lista if mess['id']==msg_id),None)
   
    if not messaggio:
        return render_template("404.html")
    else: return render_template("show.html",messaggio=messaggio)


    
if __name__=="__main__":
    app.run(debug=True)