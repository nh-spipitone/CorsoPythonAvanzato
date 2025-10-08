from flask import Flask
from task import bp as task

def main():
    app = Flask(__name__)
    app.register_blueprint(task)

    app.run()

if __name__ == "__main__":
    main()