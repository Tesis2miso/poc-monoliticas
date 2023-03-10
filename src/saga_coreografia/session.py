import mysql.connector
from utils import db_user, db_database, db_host


def connect_db():
    db = mysql.connector.connect(
        host=db_host(),
        user=db_user(),
        database=db_database()
    )
    return db
