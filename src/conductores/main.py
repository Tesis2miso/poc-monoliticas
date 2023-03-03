from flask import Flask
from flask import request
import os
import producer
import asyncio
from database import DbExecutor

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


@app.route('/health', methods=['GET'])
def Health():
    return "ok", 200


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4000))
    app.run(debug=True, host='0.0.0.0', port=port)
