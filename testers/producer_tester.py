import pulsar
from pulsar.schema import *
import uuid
import time

def time_millis():
    return int(time.time() * 1000)

class Despachador:
    def __init__(self):
        ...

    def publicar_mensaje(self, mensaje, topico):
        BROKER_HOST = 'localhost'
        cliente = pulsar.Client(f'pulsar://{BROKER_HOST}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(mensaje.__class__))
        publicador.send(mensaje)
        cliente.close()

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

class ComandoDismunirStockPayload(ComandoIntegracion):
    id_producto = String()
    id_orden = String()
    cantidad = Integer()
    direccion_entrega = String()

class ComandoDismunirStock(ComandoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = ComandoDismunirStockPayload()

despachador = Despachador()

# PROBAR
evento = ComandoDismunirStock(
        time=time_millis(),
        ingestion=time_millis(),
        datacontenttype=ComandoDismunirStockPayload.__name__,
        specversion="1",
        service_name="1",
        data = ComandoDismunirStockPayload(
            id_producto="02081bc3-52b5-4fb1-afbc-d251ebd157bd",
            id_orden=str(1),
            cantidad=1,
            direccion_entrega="Direccion"
        ) 
    )
despachador.publicar_mensaje(evento, "comando-disminuir-stock")

ComandoDismunirStockPayload()