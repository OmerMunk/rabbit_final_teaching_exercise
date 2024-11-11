from flask import Flask

from database import connection_url, init_db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = connection_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["DEBUG"] = True


with app.app_context():
    init_db()


if __name__ == "__main__":
    app.run(host='0.0.0.0',
            debug=True, #todo: maybe remove because we declared before.
            port=5001)

