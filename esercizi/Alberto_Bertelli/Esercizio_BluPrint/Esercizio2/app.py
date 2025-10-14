from flask import Flask
from tasks_blueprint import tasks_bp 

app = Flask(__name__)
app.register_blueprint(tasks_bp)

if __name__ == "__main__":
    app.run(debug=True)