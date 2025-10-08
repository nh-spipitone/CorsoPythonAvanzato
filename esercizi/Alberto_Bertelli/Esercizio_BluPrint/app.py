from flask import Flask
from tasks.routes import tasks_bp  # importa il blueprint

app = Flask(__name__)

# registra il blueprint
app.register_blueprint(tasks_bp)

if __name__ == "__main__":
    app.run(debug=True)



# app.py → avvia il server e collega i blueprint

# routes.py → contiene le funzioni che rispondono alle richieste

# jsonify() → serve per rispondere in formato JSON

# global next_id → serve per aggiornare il contatore degli ID

# tasks → è una lista che contiene tutti i task creati