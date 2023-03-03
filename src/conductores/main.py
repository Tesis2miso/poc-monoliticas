from flask import Flask
from flask import request
import os
import producer
import asyncio
from database import DbExecutor
from datetime import datetime
from eventos import StockDisminuido

app = Flask(__name__)

topico = "evento-stock"


@app.route('/tableconductor', methods=['POST'])
def CreateTableConductor():
    if request.method == 'POST':
        db = DbExecutor()
        db.create_table_conductor()

        return {"message": "OK"}


@app.route('/conductor', methods=['POST'])
def CreateConductor():
    if request.method == 'POST':
        db = DbExecutor()
        db.create_conductor()

        return {"message": "OK"}


@app.route('/conductor', methods=['PUT'])
def AssignConductor():
    if request.method == 'PUT':
        try:
            id_orden = request.json["id_orden"]
            direccion_entrega = request.json["direccion_entrega"]
        except:
            print("revert or do something")
            return {"message": ""}

        orden = StockDisminuido(id_orden=id_orden, time_stamp=str(datetime.now()), direccion_entrega=direccion_entrega)

        despachador = producer.Despachador()
        despachador.publicar_mensaje(orden, topico)

        return {"message": "OK"}


@app.route('/health', methods=['GET'])
def Health():
    return "ok", 200


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4000))
    app.run(debug=True, host='0.0.0.0', port=port)
