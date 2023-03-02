from flask import Flask
from flask import request
import os
import producer
from eventos import OrdenCreada
from database import DbExecutor

app = Flask(__name__)











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

        db = DbExecutor()
        db.create_order(id_producto, user_id, cantidad, direccion_entrega)

        orden = OrdenCreada(id_orden = 1, id_producto = id_producto, user_id= user_id, time_stamp = "3", cantidad= cantidad, direccion_entrega= direccion_entrega)

        despachador = producer.Despachador()
        despachador.publicar_mensaje(orden, "evento-orden")

        return {"message": "OK"}
            

@app.route('/health',methods = ['GET'])
def Health():
    return "ok", 200


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4000))
    app.run(debug=True, host='0.0.0.0', port=port)