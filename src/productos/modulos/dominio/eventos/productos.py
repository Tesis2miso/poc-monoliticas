from pulsar.schema import *
from dataclasses import dataclass
from productos.seedwork.dominio.eventos import (EventoDominio)

class EventoProducto(EventoDominio):
    ...

@dataclass
class StockDisminuido(EventoProducto):
    ...