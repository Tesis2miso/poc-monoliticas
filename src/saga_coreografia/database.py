from session import connect_db
from datetime import datetime


class DbExecutor:
    def __init__(self):
        pass

    def create_table_sagalog(self):
        mydb = connect_db()
        mycursor = mydb.cursor()
        sql = "CREATE TABLE sagalog (transaction_id VARCHAR(255) PRIMARY KEY, timestamp VARCHAR(255) NULL, tipo VARCHAR(255) NULL, detalle VARCHAR(255) NULL)"
        mycursor.execute(sql)
        mydb.commit()
        mydb.close()

    def insert_log(self, transaction_id, tipo, detalle):
        mydb = connect_db()
        mycursor = mydb.cursor()
        sql = "INSERT INTO sagalog (transaction_id, timestamp, tipo, detalle) VALUES (%s, %s, %s, %s)"
        values = (transaction_id, datetime.now(), tipo, detalle)
        mycursor.execute(sql, values)
        mydb.commit()
        mydb.close()
