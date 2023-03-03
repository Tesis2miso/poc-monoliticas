from pulsar.schema import *


class StockDisminuido(Record):
    time_stamp = String()
    direccion_entrega = String()
    id_orden = Integer()
