
from pulsar.schema import *

class Order(Record):
    id_orden = String()
    id_producto = String()
    user_id = String()
    time_stamp = String()
    cantidad = Integer()
    direccion_entrega = String()