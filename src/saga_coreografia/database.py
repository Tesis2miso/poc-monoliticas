from session import connect_db
from datetime import datetime


class DbExecutor:
    def __init__(self):
        pass

    def create_table_sagalog(self):
        mydb = connect_db()
        mycursor = mydb.cursor()
        sql = "CREATE TABLE sagalog (transaction_id VARCHAR(255) PRIMARY KEY, timestamp VARCHAR(255) NULL, is_compensation BOOLEAN NULL, evento VARCHAR(255) NULL, contenido VARCHAR(255) NULL)"
        mycursor.execute(sql)
        mydb.commit()
        mydb.close()

    def insert_log(self, transaction_id: str, is_compensation: bool, evento: str, contenido: str):
        mydb = connect_db()
        mycursor = mydb.cursor()
        sql = "INSERT INTO sagalog (transaction_id, timestamp, is_compensation, evento, contenido) VALUES (%s, %s, %s, %s, %s)"
        values = (transaction_id, datetime.now(), is_compensation, evento, contenido)
        mycursor.execute(sql, values)
        mydb.commit()
        mydb.close()
