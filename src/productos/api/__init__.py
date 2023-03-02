import os
from pydispatch import dispatcher
from flask import Flask, render_template, request, url_for, redirect, jsonify, session
from flask_swagger import swagger
from productos.modulos.aplicacion.handlers import HandlerProductoIntegracion
from productos.modulos.dominio.eventos.productos import StockDisminuido

# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))

def registrar_handlers():
    import productos.modulos.aplicacion

def importar_modelos_alchemy():
    import productos.modulos.infraestructura.dto

def comenzar_consumidor(app):
    import threading
    import productos.modulos.infraestructura.consumidores as productos

    # Suscripción a eventos
    # No uso eventos

    # Suscripción a comandos
    threading.Thread(target=productos.suscribirse_a_comando_disminuir_stock, args=[app]).start()

def comenzar_dispatchers(app):
    dispatcher.connect(HandlerProductoIntegracion.handle_stock_disminuido, signal=f'{StockDisminuido.__name__}Integracion')

def create_app(configuracion={}):
    # Init la aplicacion de Flask
    app = Flask(__name__, instance_relative_config=True)
    
    app.secret_key = '9d58f98f-3ae8-4149-a09f-3a8c2012e32c'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['TESTING'] = configuracion.get('TESTING')

     # Inicializa la DB
    from productos.config.db import init_db, database_connection

    app.config['SQLALCHEMY_DATABASE_URI'] = database_connection(configuracion, basedir=basedir)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_db(app)

    from productos.config.db import db

    importar_modelos_alchemy()
    registrar_handlers()

    with app.app_context():
        db.create_all()
        if not app.config.get('TESTING'):
            comenzar_consumidor(app)
            comenzar_dispatchers(app)
        
        # TODO Saga
        #from productos.modulos.sagas.aplicacion.coordinadores.saga_reservas import CoordinadorReservas
        #CoordinadorReservas()

     # Importa Blueprints
    from . import productos

    # Registro de Blueprints
    app.register_blueprint(productos.bp)

    @app.route("/spec")
    def spec():
        swag = swagger(app)
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "Productos"
        return jsonify(swag)

    @app.route("/health")
    def health():
        return {"status": "up"}

    return app
