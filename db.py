import mysql.connector
from flask import Flask

app = Flask(__name__)


def get_db():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='spice_store'
    )
    return conn


@app.teardown_appcontext
def close_db(error):
    if hasattr(Flask, 'db'):
        Flask.db.close()


if __name__ == '__main__':
    app.run(debug=True)
