

import mysql.connector

class DbExecutor:
    def __init__(self):
        self.db =  mysql.connector.connect(
                    host="34.68.216.107",
                    user="root",
                    database="monoliticas"
                )
    

    def create_order(self, id_producto, user_id, cantidad, direccion_entrega ):
        mycursor = self.db.cursor()
        sql = "INSERT INTO ordenes (id_producto, user_id, time_stamp, cantidad, direccion_entrega) VALUES (%s, %s, %s, %s, %s)"
        values = (id_producto, user_id, 6, cantidad, direccion_entrega)
        mycursor.execute(sql, values)
        self.db.commit()
        self.db.close()