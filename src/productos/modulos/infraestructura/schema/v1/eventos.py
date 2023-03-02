from pulsar.schema import *
from productos.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion
from productos.seedwork.infraestructura.utils import time_millis
import uuid

class StockDisminuidoPayload(Record):
    id_producto = String()
    id_orden = String()
    cantidad = Integer()
    direccion_entrega = String()

class EventoStockDisminuido(EventoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = StockDisminuidoPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class OrdenCreadaPayload(Record):
    id_producto = String()
    id_orden = String()
    cantidad = Integer()
    direccion_entrega = String()

class EventoOrdenCreada(EventoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = OrdenCreadaPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)