from flask import Flask
from flask import request
import datetime
import os
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
  host="34.68.216.107",
  user="root",
  database="monoliticas"
)

@app.route('/orden',methods = ['POST'])
def CreateOrden():
    
    if request.method == 'POST':
        try:
            id_producto = request.json["id_producto"]
            user_id = request.json["user_id"]
            cantidad = request.json["cantidad"]
            direccion_entrega = request.json["direccion_entrega"]
        except:
            print("revert or do something")
            return {"message": ""} 



        mycursor = mydb.cursor()
        sql = "INSERT INTO ordenes (id_producto, user_id, time_stamp, cantidad, direccion_entrega) VALUES (%s, %s, %s, %s, %s)"
        values = (id_producto, user_id, 6, cantidad, direccion_entrega)
        mycursor.execute(sql, values)
        mydb.commit()

        return {"message": "OK"}
            

@app.route('/health',methods = ['GET'])
def Health():
    return "ok", 200


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4000))
    app.run(debug=True, host='0.0.0.0', port=port)