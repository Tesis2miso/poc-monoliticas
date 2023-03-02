import logging
import traceback
import pulsar, _pulsar
from pulsar.schema import *
from productos.seedwork.infraestructura import utils
from productos.modulos.infraestructura.schema.v1.eventos import EventoStockDisminuido
from productos.modulos.infraestructura.schema.v1.comandos import ComandoDismunirStock

def suscribirse_a_topico(topico: str, suscripcion: str, schema: Record, app=None):
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
            # TODO Ejecutar proyecciones
            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comando_disminuir_stock(app=None):
    suscribirse_a_topico("comando-disminuir-stock", "sub-com-disminuir-stock", ComandoDismunirStock, app)

def suscribirse_a_evento_stock_disminuido(app=None):
    suscribirse_a_topico("evento-stock-disminuido", "sub-stock-disminuido", EventoStockDisminuido, app)