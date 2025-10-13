from enum import Enum
import json
from os import path

class statusEnum(Enum):
    PRESENT="present"
    ABSENT="absent"
    LATE="late"

BASE_DIR = path.dirname(path.abspath(__file__))
DB_PATH = path.join(BASE_DIR, "db.json")

db_base = {"students": [], "grades": [], "attendance": []}

def reset_db():
    try:
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(db_base, f)
            return db_base
    except: 
        return ("Errore nella creazione JSON")  
    
def load_db():
    if not path.exists(DB_PATH):    
        return reset_db()
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        return reset_db()

def save_db(db):
    try:
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(db, f)
            return db
    except: 
        return ("Errore nel salvataggio db")

def next_id(seq):
    return (max([r.get("id", 0) for r in seq]) + 1) if seq else 1

def get_student(db, student_id):
    return next((s for s in db.get("students", []) if s.get("id") == student_id), None)

def compute_summary(db, student_id):
    summary = {
        "avg": 0.0,
        "count": 0,
        "present": 0,
        "absent": 0,
        "late": 0,
        "minutes_late": 0,
    }

    grades = db.get("grades", [])
    attendances = db.get("attendance", [])
    
    grades_by_id = [g for g in grades if(g.get("student_id", []) == student_id)]
    attendances_by_id = [a for a in attendances if(a.get("student_id", []) == student_id)]

    total_grade_value = 0.0
    
    for g in grades_by_id:
        total_grade_value += g.get("value", 0.0)
        
    summary["count"] = len(grades_by_id)

    if summary["count"] > 0:
        summary["avg"] = round(total_grade_value / summary["count"], 2)
    
    for a in attendances_by_id:
        status = a.get("status", "unknown").lower()
        
        if status == "present":
            summary["present"] += 1
        elif status == "absent":
            summary["absent"] += 1
        elif status == "late":
            summary["late"] += 1
            
        summary["minutes_late"] += a.get("minutes_late", 0)

    return summary