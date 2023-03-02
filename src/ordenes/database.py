

import mysql.connector
from session import connect_db
from datetime import datetime

class DbExecutor:
    def __init__(self):
        pass

    def create_order(self, id_producto, user_id, cantidad, direccion_entrega ):
        mydb = connect_db()
        mycursor = mydb.cursor()
        sql = "INSERT INTO ordenes (id_producto, user_id, time_stamp, cantidad, direccion_entrega) VALUES (%s, %s, %s, %s, %s)"
        values = (id_producto, user_id, datetime.now(), cantidad, direccion_entrega)
        mycursor.execute(sql, values)
        mydb.commit()
        mydb.close()