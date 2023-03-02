from pulsar.schema import *
from dataclasses import dataclass
from productos.seedwork.dominio.eventos import (EventoDominio)

class EventoProducto(EventoDominio):
    ...

@dataclass
class ProductoCreado(EventoProducto):
    id_producto = String()
    fecha_creacion = Long()

@dataclass
class InventarioDisminuido(EventoProducto):
    product_id = String()
    stock = Integer()
    fecha_modificacion = Long()

@dataclass
class InventarioAumentado(EventoProducto):
    product_id = String()
    stock = Integer()
    fecha_modificacion = Long()