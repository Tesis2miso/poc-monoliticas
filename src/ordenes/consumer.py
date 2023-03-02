
import pulsar
from pulsar.schema import *
from utils import broker_host
from eventos import OrdenCreada
from database import DbExecutor

topico = "evento-ordenes"

def escuchar_mensaje(topico,  schema=Record):
    cliente = pulsar.Client(f'pulsar://{broker_host()}:6650')
    consumer = cliente.subscribe(topico,schema=AvroSchema(schema), subscription_name='evento')
    while True:
        msg = consumer.receive()
        message = msg.value()

        consumer.acknowledge(msg)

        id_producto = message.id_orden
        user_id = message.user_id
        cantidad = message.cantidad
        direccion_entrega = message.direccion_entrega

        db = DbExecutor()
        db.create_order(id_producto, user_id, cantidad, direccion_entrega)


    cliente.close()

escuchar_mensaje(topico, OrdenCreada)