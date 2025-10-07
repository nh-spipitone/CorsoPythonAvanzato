from flask import Flask, render_template, request, redirect,url_for,flash
import json
from os import path,mkdir
app = Flask(__name__)
if(not path.exists("data/messages.json") ):
    mkdir("data")
    messaggi=open("./data/messages.json","x")
    messaggi.close()
    

@app.route("/")
def home():
    messaggi_json =open("./data/messages.json","r")
    messaggi=json.load(messaggi_json)
    messaggi_json.close()
    return render_template("home.html",messages=messaggi)

@app.route("/new",methods=["GET", "POST"])
def newmsg():
    if(request.method=="POST"):
        author=request.form['author']
        text=request.form['text']
        newmessage={"author":author,"text":text}
        messaggi=open("data/messages.json","w+")
        json.dump(newmessage,messaggi)
        messaggi.close()
        return redirect(url_for("home"))
    else:
        return render_template("new.html")
    
if __name__=="__main__":
    app.run(debug=True)