from flask import Flask
from flask import request, jsonify
import os
import dispatchers
from model import Order

app = Flask(__name__)

@app.route('/start',methods = ['POST'])
def PublishOrder():

    if request.method == 'POST':
        try:
            id_producto = request.json["id_producto"]
            user_id = request.json["user_id"]
            cantidad = request.json["cantidad"]
            direccion_entrega = request.json["direccion_entrega"]
        except:
            return jsonify({ 'mssg': 'Bad request'}), 400

        orden = Order(id_producto = id_producto, user_id= user_id, cantidad= cantidad, direccion_entrega= direccion_entrega)

        disp = dispatchers.Despachador()
        disp.publicar_mensaje(orden, "evento-orden")

        return jsonify({ 'mssg': 'Procesando mensaje'}), 203
            

@app.route('/health',methods = ['GET'])
def Health():
    return jsonify({ 'mssg': 'Error'}), 200


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4000))
    app.run(debug=True, host='0.0.0.0', port=port)