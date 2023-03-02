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

class ComandoCrearProductoPayload(ComandoIntegracion):
    nombre = String()
    stock = Integer()

class ComandoCrearProducto(ComandoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = ComandoCrearProductoPayload()

despachador = Despachador()

# PROBAR
evento = ComandoDismunirStock(
        time=time_millis(),
        ingestion=time_millis(),
        datacontenttype=ComandoDismunirStockPayload.__name__,
        specversion="1",
        service_name="1",
        data = ComandoDismunirStockPayload(
            id_producto="63850469-2e1f-4f16-bb5b-39e4035a00b9",
            id_orden=str(1),
            cantidad=1,
            direccion_entrega="Direccion"
        ) 
    )
despachador.publicar_mensaje(evento, "comando-disminuir-stock")

#evento = ComandoCrearProducto(
#        time=time_millis(),
#        ingestion=time_millis(),
#        datacontenttype=ComandoCrearProductoPayload.__name__,
#        specversion="1",
#        service_name="1",
#        data = ComandoCrearProductoPayload(
#            nombre="Buenas1",
#            stock=13,
#        ) 
#    )
#despachador.publicar_mensaje(evento, "comando-crear-producto")
