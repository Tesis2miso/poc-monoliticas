

import mysql.connector
from session import connect_db, connect_db_replica
from datetime import datetime

class DbExecutor:
    def __init__(self):
        pass

    def create_order(self,id_orden, id_producto, user_id, cantidad, direccion_entrega):
        mydb = connect_db()
        mycursor = mydb.cursor()
        sql = "INSERT INTO ordenes (id_orden, id_producto, user_id, time_stamp, cantidad, direccion_entrega, estado) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (id_orden, id_producto, user_id, datetime.now(), cantidad, direccion_entrega, "creada")
        mycursor.execute(sql, values)
        mydb.commit()
        mydb.close()

    def update_order_status(self, id_orden, id_conductor):
        mydb = connect_db()
        mycursor = mydb.cursor()
        sql = "UPDATE ordenes SET estado = 'iniciada',id_driver = %s  where id_orden = %s"
        values = (id_conductor, id_orden)
        mycursor.execute(sql, values)
        mydb.commit()
        mydb.close()

    def update_order_status_failed(self, id_orden):
        mydb = connect_db()
        mycursor = mydb.cursor()
        sql = "UPDATE ordenes SET estado = 'fallida' WHERE id_orden = %s"
        values = (id_orden,)
        mycursor.execute(sql, values)
        mydb.commit()
        mydb.close()


class DbExecutorReplica:
    def __init__(self):
        pass

    def create_order(self,id_orden, id_producto, user_id, cantidad, direccion_entrega ):
        mydb = connect_db_replica()
        mycursor = mydb.cursor()
        sql = "INSERT INTO ordenes (id_orden, id_producto, user_id, time_stamp, cantidad, direccion_entrega, estado) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (id_orden, id_producto, user_id, datetime.now(), cantidad, direccion_entrega, "creada")
        mycursor.execute(sql, values)
        mydb.commit()
        mydb.close()

    def update_order_status(self, id_orden, id_conductor):
        mydb = connect_db_replica()
        mycursor = mydb.cursor()
        sql = "UPDATE ordenes SET estado = 'iniciada',id_driver = %s  where id_orden = %s"
        values = (id_conductor, id_orden)
        mycursor.execute(sql, values)
        mydb.commit()
        mydb.close()

    def update_order_status_failed(self, id_orden):
        mydb = connect_db_replica()
        mycursor = mydb.cursor()
        sql = "UPDATE ordenes SET estado = 'fallida' WHERE id_orden = %s"
        values = (id_orden,)
        mycursor.execute(sql, values)
        mydb.commit()
        mydb.close()