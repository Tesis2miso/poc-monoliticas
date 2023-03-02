
from pulsar.schema import *

class Order(Record):
    id_orden = int()
    id_producto = int()
    user_id = int()
    time_stamp = String()
    cantidad = int()
    direccion_entrega = String()