from session import connect_db
from datetime import datetime

class DbExecutor:
    def __init__(self):
        pass

    def create_table_conductor(self):
        mydb = connect_db()
        mycursor = mydb.cursor()
        sql = "CREATE TABLE conductores (id_conductor INT AUTO_INCREMENT PRIMARY KEY, id_orden INT NULLABLE, direccion_entrega VARCHAR(255) NULLABLE, time_stamp VARCHAR(255) NULLABLE)"
        mycursor.execute(sql)
        mydb.commit()
        mydb.close()

    def create_conductor(self):
        mydb = connect_db()
        mycursor = mydb.cursor()
        sql = "INSERT INTO conductores (id_orden, direccion_entrega, time_stamp) VALUES (NULL, NULL, NULL)"
        mycursor.execute(sql)
        mydb.commit()
        mydb.close()

    def get_unassigned_conductor(self):
        mydb = connect_db()
        mycursor = mydb.cursor()
        sql = "SELECT id_conductor FROM conductores WHERE id_orden IS NULL"
        mycursor.execute(sql)
        id_conductor = mycursor.fetchone()
        mydb.commit()
        mydb.close()

        return id_conductor

    def assign_conductor(self, id_conductor, id_orden, direccion_entrega):
        mydb = connect_db()
        mycursor = mydb.cursor()
        sql = "UPDATE conductores SET id_orden = %s, direccion_entrega = %s, time_stamp = %s WHERE id_conductor = %s"
        values = (id_orden, direccion_entrega, datetime.now(), id_conductor)
        mycursor.execute(sql, values)
        mydb.commit()
        mydb.close()
