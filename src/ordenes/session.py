import mysql.connector
from utils import db_user, db_database, db_host, db_user_replica, db_host_replica, db_database_replica


def connect_db():
    db = mysql.connector.connect(
        host=db_host(),
        user=db_user(),
        database=db_database()
    )
    return db

def connect_db_replica():
    db = mysql.connector.connect(
        host=db_host_replica(),
        user=db_user_replica(),
        database=db_database_replica()
    )
    return db
