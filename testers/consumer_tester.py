import pulsar, _pulsar
from pulsar.schema import *
import logging
import traceback
import uuid
import time
import os

def time_millis():
    return int(time.time() * 1000)

class Mensaje(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()

    def __init__(self, *args, id=None, **kwargs):
        super().__init__(*args, id=id, **kwargs)

class ComandoIntegracion(Mensaje):
    ...

class ComandoAsignarConductorPayload(ComandoIntegracion):
    id_producto = String()
    id_orden = String()
    cantidad = Integer()
    direccion_entrega = String()

class ComandoAsignarConductor(ComandoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = ComandoAsignarConductorPayload()

def suscribirse_a_topico(topico: str, suscripcion: str):
    cliente = None
    BROKER_HOST = os.getenv('BROKER_HOST', default="localhost")
    try:
        cliente = pulsar.Client(f'pulsar://{BROKER_HOST}:6650')
        consumidor = cliente.subscribe(
            topico,
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name=suscripcion,
            schema=AvroSchema(ComandoAsignarConductor)
        )
        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print("\n")
            print(datos)
            consumidor.acknowledge(mensaje)     
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()


# PROBAR
suscribirse_a_topico("comando-asignar-conductor", "sub-com-asignar-conductor")