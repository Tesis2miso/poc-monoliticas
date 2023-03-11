import uuid
from pulsar.schema import *
from utils import time_millis


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
    transaction_id = String()


class ComandoAsignarConductor(ComandoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = ComandoAsignarConductorPayload()


class ComandoRevertirDisminuirStockPayload(ComandoIntegracion):
    id_producto = String()
    id_orden = String()
    cantidad = Integer()
    direccion_entrega = String()
    transaction_id = String()


class ComandoRevertirDisminuirStock(ComandoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = ComandoRevertirDisminuirStockPayload()


class ComandoMarcarListoDespachoPayload(ComandoIntegracion):
    id_orden = String()
    id_conductor = String()
    direccion_entrega = String()
    transaction_id = String()


class ComandoMarcarListoDespacho(ComandoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = ComandoMarcarListoDespachoPayload()
