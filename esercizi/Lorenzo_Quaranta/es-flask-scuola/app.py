'''
Realizza una mini web‑app Flask che emula un sito scolastico con:

elenco studenti,
dettaglio studente con media voti e presenze/assenze/ritardi,
moduli per inserire nuovi voti e nuove presenze,
salvataggio su file JSON (db.json), senza database esterni.
'''
from flask import Flask, render_template, request, redirect,url_for,flash
import json, os, datetime

app = Flask(__name__)
#init e controllo esistenza file json
default_json_structure={ "students": [], "grades": [], "attendance": [] }

if( not os.path.exists("db.json")):
       with open("db.json","x",encoding="utf-8") as db_json:
              json.dump(default_json_structure,db_json,indent=2, ensure_ascii=False)

def load_db():
      with open("db.json", "r", encoding="utf-8") as db_file:
             return json.load(db_file)

def save_db(db):
      with open("db.json","w",encoding="utf-8") as db_json:
              json.dump(db,db_json,indent=2, ensure_ascii=False)


def next_id(seq):
      return(seq[-1]["id"]+1) if seq else 1

def get_student(id):
        db=load_db()
        student={}
        student["grades_avg"]=0
        student["grades_num"]=0
        student["times_present"]=0
        student["times_absent"]=0
        student["times_late"]=0
        student["late_minutes_sum"]=0
        sum_grades=0
        for s in db["students"]:
                if s["id"]==id:
                        student["name"]=s["name"]
        for g in db["grades"]:
             if g["student_id"]==id:
                    student["grades_num"]+=1
                    sum_grades+=g["grade"]
                    student["grades_avg"]=sum_grades/student["grades_num"]
        for a in db["attendance"]:
                if a["stud_id"]==id:
                        if a["status"]=="late":
                               student["times_late"]+=1
                               student["late_minutes_sum"]+=a["minutes_late"]
                        elif a["status"]=="absent":
                               student["times_absent"]+=1
                        elif a["status"]=="present":
                               student["times_present"]+=1
                        
                               
                
         

@app.route("/")
def show_dashboard():
         db= load_db()

@app.route("/students")
def show_students():
        studenti= load_db()["students"]

@app.route("/students/<int:student_id>")
def show_single_student(student_id):
        student=get_student(id)

@app.route("/students/<id>/grade/new",methods=["GET","POST"])
def new_grade(id):
        if request.method=="POST":
               materia=request.form["materia"]
               valore=request.form["valore"]
               data=request.form["data"]
               db=load_db()
               new_grade={}
               new_grade["materia"]=materia
               new_grade["valore"]=valore
               new_grade["data"]=data
               new_grade["stud_id"]=id
               db["grade"].append(new_grade)
               save_db(db)

@app.route("/students/<id>/attendance/new",methods=["GET","POST"])
def attendance(id):
        if request.method=="POST":
               present=request.form["present"]
               absent=request.form["absent"]
               late=request.form["late"]
               minutes_late=request.form["minutes_late"]
               db=load_db()
               new_attendance={}
               new_attendance["present"]=present
               new_attendance["absent"]=absent
               new_attendance["late"]=late
               new_attendance["minutes_late"]=minutes_late
               new_attendance["stud_id"]=id
               db["attendance"].append(new_attendance)
               save_db(db)

@app.route("/api/students")
def load_students():
        return load_db()["students"]

@app.route("/api/students/<id>")
def get_single_student(id):
        return get_student(id)

@app.route("/api/students/<id>/grades",methods=["POST"])
def upload_student_grade(id):
        data=request.json
        db=load_db()
        new_grade={}
        new_grade["materia"]=data["materia"]
        new_grade["valore"]=data["valore"]
        new_grade["data"]=data["data"]
        new_grade["stud_id"]=id
        db["grade"].append(new_grade)
        save_db(db)

@app.route("/api/students/<id>/attendance",methods=["POST"])
def upload_student_attendance(id):
        data=request.json
        db=load_db()
        new_attendance={}
        new_attendance["present"]=data["present"]
        new_attendance["absent"]=data["absent"]
        new_attendance["late"]=data["late"]
        new_attendance["minutes_late"]=data["minutes_late"]
        new_attendance["stud_id"]=id
        db["attendance"].append(new_attendance)
        save_db(db)
 
if __name__=="__main__":
    app.run(debug=True)