

import mysql.connector
from bff.session import connect_db
from datetime import datetime

class DbExecutor:
    def __init__(self):
        pass

    def get_orders(self):
        mydb = connect_db()
        mycursor = mydb.cursor()
        sql = "SELECT * FROM ordenes"
        mycursor.execute(sql)
        ordenes = mycursor.fetchall()
        mydb.commit()
        mydb.close()

        response = []

        for order in ordenes:
            response.append(self.create_order_response(order))

        return response
    
    def get_orders_id(self, id_orden):
        mydb = connect_db()
        mycursor = mydb.cursor()
        sql = "SELECT * FROM ordenes where id_orden = %s"
        values = (id_orden,)
        mycursor.execute(sql, values)
        orden = mycursor.fetchall()
        print(orden)
        mydb.commit()
        mydb.close()

        return self.create_order_response(orden[0])

    def create_order_response(self,input):
        res = {
            "id_producto":input[0] if input[0] else "",
            "id_orden": input[1] if input[1] else "",
            "user_id": input[2] if input[2] else "",
            "time_stamp": input[3] if input[3] else "",
            "cantidad":input[4] if input[4] else "",
            "direccion_entrega":input[5] if input[5] else "",
            "estado":input[6] if input[6] else "",
            "id_driver":input[7] if input[7] else "",
        }
        return res

    