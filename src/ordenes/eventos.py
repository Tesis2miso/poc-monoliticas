
from pulsar.schema import *

class OrdenCreada(Record):
    id_orden = Integer()
    id_producto = Integer()
    user_id = Integer()
    time_stamp = String()
    cantidad = Integer()
    direccion_entrega = String()