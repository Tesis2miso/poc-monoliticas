import uuid

from flask import Flask, request, jsonify
import os
from bff import dispatchers
from bff.model import Order
import xmltodict, json
import requests
from bff.database import DbExecutor

app = Flask(__name__)


@app.route('/orders', methods=['POST'])
def PublishOrder():
    if request.method == 'POST':
        try:
            if (request.headers['Content-Type'] == 'application/xml'):
                objJson = xmltodict.parse(request.get_data())
                id_producto = objJson[list(objJson)[0]].get('id_producto')
                user_id = objJson[list(objJson)[0]].get('user_id')
                cantidad = int(objJson[list(objJson)[0]].get('cantidad'))
                direccion_entrega = objJson[list(objJson)[0]].get('direccion_entrega')
            else:
                id_producto = request.json["id_producto"]
                user_id = request.json["user_id"]
                cantidad = request.json["cantidad"]
                direccion_entrega = request.json["direccion_entrega"]
        except:
            return jsonify({'mssg': 'Bad request'}), 400

        orden = Order(id_producto=id_producto, user_id=user_id,
                      cantidad=cantidad, direccion_entrega=direccion_entrega, transaction_id=str(uuid.uuid4()))

        disp = dispatchers.Despachador()
        disp.publicar_mensaje(orden, "evento-ordenes-2")

        return jsonify({'mssg': 'Procesando mensaje'}), 203


@app.route('/orders', methods=['GET'])
def GetOrders():
    if request.method == 'GET':
        db = DbExecutor()
        orders = db.get_orders()
        return orders


@app.route('/orders/<id>', methods=['GET'])
def GetOrdersByID(id):
    if request.method == 'GET':
        db = DbExecutor()
        print(type(id))
        order = db.get_orders_id(id)
        return order


@app.route('/productos', methods=['GET'])
def GetProducts():
    products_url = os.getenv("PRODUCTS_URL", default="localhost:3000")
    response = requests.get(f'http://{products_url}/productos')
    return response.json(), response.status_code


@app.route('/productos/<id>', methods=['GET'])
def GetProduct(id):
    products_url = os.getenv("PRODUCTS_URL", default="localhost:3000")
    response = requests.get(f'http://{products_url}/productos/{id}')
    return response.json(), response.status_code


@app.route('/health', methods=['GET'])
def Health():
    return jsonify({'mssg': 'Error'}), 200


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4000))
    app.run(debug=True, host='0.0.0.0', port=port)
