import logging
import traceback
import pulsar, _pulsar
from pulsar.schema import *
from productos.seedwork.infraestructura import utils
from productos.modulos.infraestructura.schema.v1.comandos import ComandoDismunirStock, ComandoCrearProducto, ComandoRevertirDisminuirStock
from productos.seedwork.aplicacion.comandos import ejecutar_commando
from productos.modulos.aplicacion.comandos.disminuir_stock import DisminuirStock
from productos.modulos.aplicacion.comandos.revertir_disminuir_stock import RevertirDisminuirStock
from productos.modulos.aplicacion.comandos.crear_producto import CrearProducto
from productos.modulos.aplicacion.mapeadores import MapeadorProductoDTOJson
from productos.seedwork.infraestructura.proyecciones import ejecutar_proyeccion
from productos.modulos.infraestructura.proyecciones import ProyeccionModificacionProducto
from productos.modulos.dominio.entidades import Producto


def suscribirse_a_evento(topico: str, suscripcion: str, schema: Record, funcion_evento, app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe(
            topico,
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name=suscripcion,
            schema=AvroSchema(schema)
        )
        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print("\n")
            print(datos)
            print(f'Evento recibido: {datos}')
            funcion_evento(datos, app)
            consumidor.acknowledge(mensaje)
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()


def suscribirse_a_comando(topico: str, suscripcion: str, schema: Record, funcion_comando, app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe(
            topico,
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name=suscripcion,
            schema=AvroSchema(schema)
        )
        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print("\n")
            print(datos)
            print(f'Comando recibido: {datos}')
            funcion_comando(datos, app)
            consumidor.acknowledge(mensaje)
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()


def suscribirse_a_comando_disminuir_stock(app=None):
    def procesar(datos, app):
        try:
            with app.app_context():
                comando = DisminuirStock(
                    datos.id_producto, datos.id_orden,
                    datos.cantidad, datos.direccion_entrega, datos.transaction_id
                )
                producto: Producto = ejecutar_commando(comando)
                ejecutar_proyeccion(
                    ProyeccionModificacionProducto(
                        producto.id, producto.nombre,
                        producto.stock, producto.fecha_creacion,
                        producto.fecha_actualizacion
                    ), app=app
                )
        except:
            logging.error('ERROR: Procesando eventos!')
            traceback.print_exc()

    suscribirse_a_comando(
        "comando-disminuir-stock", "sub-com-disminuir-stock",
        ComandoDismunirStock, procesar, app
    )


def suscribirse_a_comando_crear_producto(app=None):
    def procesar(datos, app):
        try:
            with app.app_context():
                map_reserva = MapeadorProductoDTOJson()
                producto_dto = map_reserva.externo_a_dto({
                    'nombre': datos.nombre,
                    'stock': datos.stock
                })
                comando = CrearProducto(
                    producto_dto.fecha_creacion,
                    producto_dto.fecha_actualizacion, producto_dto.id,
                    producto_dto.nombre, producto_dto.stock
                )
                producto: Producto = ejecutar_commando(comando)
                ejecutar_proyeccion(
                    ProyeccionModificacionProducto(
                        producto.id, producto.nombre,
                        producto.stock, producto.fecha_creacion,
                        producto.fecha_actualizacion
                    ), app=app
                )
        except:
            logging.error('ERROR: Procesando eventos!')
            traceback.print_exc()

    suscribirse_a_comando(
        "comando-crear-producto", "sub-com-crear-producto",
        ComandoCrearProducto, procesar, app
    )


def suscribirse_a_comando_revertir_disminuir_stock(app=None):
    def procesar(datos, app):
        try:
            with app.app_context():
                comando = RevertirDisminuirStock(
                    datos.id_producto, datos.id_orden,
                    datos.cantidad, datos.direccion_entrega, datos.transaction_id
                )
                producto: Producto = ejecutar_commando(comando)
                ejecutar_proyeccion(
                    ProyeccionModificacionProducto(
                        producto.id, producto.nombre,
                        producto.stock, producto.fecha_creacion,
                        producto.fecha_actualizacion
                    ), app=app
                )
        except:
            logging.error('ERROR: Procesando eventos!')
            traceback.print_exc()

    suscribirse_a_comando(
        "comando-asignar-conductor", "sub-com-asignar-conductor",
        ComandoRevertirDisminuirStock, procesar, app
    )
