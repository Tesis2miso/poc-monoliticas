from pulsar.schema import *
from dataclasses import dataclass
from productos.seedwork.dominio.eventos import (EventoDominio)
import uuid

class EventoProducto(EventoDominio):
    ...

@dataclass
class StockDisminuido(EventoProducto):
    id_producto: uuid.UUID = None
    id_orden: uuid.UUID = None
    cantidad: int = None
    direccion_entrega: str = None