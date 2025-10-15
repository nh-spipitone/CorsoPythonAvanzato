import psycopg2
from flask import Flask


def create_app() -> Flask:
    conn = psycopg2.connect("dbname=esempio user=postgres")
    with open("db_schema.sql") as file:
        cur = conn.cursor()
        cur.execute("".join(file.readlines()))
    conn.commit()

    app = Flask(__name__)


    from .user import bp
    app.register_blueprint(bp)
    app.secret_key = "prova1234"
    bp.conn = conn
    return app
