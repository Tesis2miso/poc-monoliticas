from .main import *


def connect_db():
    db = mysql.connector.connect(
    host="34.68.216.107",
    user="root",
    database="monoliticas"
    )
    return db

mydb = connect_db()