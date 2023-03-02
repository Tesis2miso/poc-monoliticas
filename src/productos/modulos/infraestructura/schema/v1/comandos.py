from pulsar.schema import *
from dataclasses import dataclass, field
from productos.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)
from productos.seedwork.infraestructura.utils import time_millis
import uuid

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