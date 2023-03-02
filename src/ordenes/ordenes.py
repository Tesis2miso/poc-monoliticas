from flask import Flask
from flask import request
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
            request.json["id_producto"]
            request.json["user_id"]
            request.json["time_stamp"]
            request.json["cantidad"]
            request.json["direccion_entrega"]
        except:
            print("revert or do something")
            return {"message": ""} 


        mycursor = mydb.cursor()

        # Execute a query
        mycursor.execute("SELECT * FROM ordenes")

        # Fetch the results
        results = mycursor.fetchall()

        # Print the results
        for row in results:
            print(row)


        return {"message": "OK"}
            

@app.route('/health',methods = ['GET'])
def Health():
    return "ok", 200


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4000))
    app.run(debug=True, host='0.0.0.0', port=port)