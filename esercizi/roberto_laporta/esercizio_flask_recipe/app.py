from flask import Flask
from models import db
from auth import bp_auth
from recipe import bp_recipes
from seeds import seed_db

import secrets

def create_app():
        
    app = Flask(__name__)

    app.config["SECRET_KEY"] = secrets.token_hex(16)
    app.config["JWT_SECRET_KEY"] = app.config["SECRET_KEY"] 

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://app:app@db:5432/appdb"

    db.init_app(app)

    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_recipes)

    # API

    @app.get("/healthy_check")
    def healthy_check():
        return "App is running..."
    
    @app.cli.command("init_db")
    def init_db_command():
        db.create_all()
        print("Tabelle del database create o verificate.")
        
        seed_db()
        
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)