from flask import Flask
from tasks.routes import tasks_bp  # importa il blueprint

app = Flask(__name__)

# registra il blueprint
app.register_blueprint(tasks_bp)

if __name__ == "__main__":
    app.run(debug=True)