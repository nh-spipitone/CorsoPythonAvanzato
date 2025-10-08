from flask import Flask, render_template, request, redirect, url_for, flash, abort, session
import os
import json
app = Flask(__name__)  # Crea un'applicazione Flask
app.secret_key = "dev"

DATA_FILE = 'data/messages.json'
def load_messages():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []
        
def save_messages(messages):
    os.makedirs('data', exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages, f, indent=2)

def get_next_id(messages):
    if not messages:
        return 1
    return max(msg['id'] for msg in messages) + 1

@app.get("/")
def home():
     page = request.args.get('page', default=1, type=int)
     per_page = 10

     all_messages = load_messages()
     sorted_messages = sorted(all_messages, key=lambda x: x['id'], reverse=True)
    
     start = (page - 1) * per_page
     end = start + per_page
     paginated = sorted_messages[start:end]

     total_pages = (len(all_messages) + per_page - 1) // per_page

     return render_template('home.html', messages=paginated, page=page, total_pages=total_pages)