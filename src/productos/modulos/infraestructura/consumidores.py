import logging
import traceback
import pulsar, _pulsar
from pulsar.schema import *
from productos.seedwork.infraestructura import utils
from productos.modulos.infraestructura.schema.v1.comandos import ComandoDismunirStock
from productos.seedwork.aplicacion.comandos import ejecutar_commando
from productos.modulos.aplicacion.comandos.disminuir_stock import DisminuirStock

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
                    datos.cantidad, datos.direccion_entrega
                )
                ejecutar_commando(comando)
        except:
            logging.error('ERROR: Procesando eventos!')
            traceback.print_exc()
    suscribirse_a_comando(
        "comando-disminuir-stock", "sub-com-disminuir-stock",
        ComandoDismunirStock, procesar, app
    )