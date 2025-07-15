from flask import g
import psycopg2

from helpers.application import app

DATABASE = 'censoescolar.db'


def getConnection():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = psycopg2.connect(user="postgres",
                                            password="123456",
                                            host="127.0.0.1",
                                            port="5434",
                                            database="censoescolar")
    return db


@app.teardown_appcontext
def closeConnection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
