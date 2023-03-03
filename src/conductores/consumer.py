import pulsar
from pulsar.schema import *
from utils import broker_host
from eventos import StockDisminuido
from database import DbExecutor

topico = "evento-stock"


def escuchar_mensaje(topico, schema=Record):
    cliente = pulsar.Client(f'pulsar://{broker_host()}:6650')
    consumer = cliente.subscribe(topico, schema=AvroSchema(schema), subscription_name='evento')
    while True:
        msg = consumer.receive()
        message = msg.value()

        consumer.acknowledge(msg)

        id_orden = message.id_orden
        direccion_entrega = message.direccion_entrega
        db = DbExecutor()

        id_conductor = db.get_unassigned_conductor()

        if id_conductor:
            db.assign_conductor(id_conductor, id_orden, direccion_entrega)
        else:
            raise Exception("No hay ningun conductor disponible, regla de negocio")

    cliente.close()


escuchar_mensaje(topico, StockDisminuido)
