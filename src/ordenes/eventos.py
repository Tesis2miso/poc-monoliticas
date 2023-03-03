import uuid

from pulsar.schema import *

from utils import time_millis

class OrdenCreada(Record):
    id_orden = String()
    id_producto = String()
    user_id = String()
    time_stamp = String()
    cantidad = Integer()
    direccion_entrega = String()


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