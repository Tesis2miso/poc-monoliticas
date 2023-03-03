import pulsar
from pulsar.schema import *
from utils import broker_host
from eventos import ComandoAsignarConductor, ComandoMarcarListoDespacho, ComandoMarcarListoDespachoPayload
from database import DbExecutor
from utils import time_millis
import producer


def escuchar_mensaje(topico, schema=Record):
    cliente = pulsar.Client(f'pulsar://{broker_host()}:6650')
    consumer = cliente.subscribe(topico, schema=AvroSchema(schema), subscription_name='evento')
    while True:
        msg = consumer.receive()
        message = msg.value()

        consumer.acknowledge(msg)

        id_orden = message.data.id_orden
        direccion_entrega = message.data.direccion_entrega
        db = DbExecutor()

        id_conductor = db.get_unassigned_conductor()

        if id_conductor:
            db.assign_conductor(id_conductor, id_orden, direccion_entrega)

            evento = ComandoMarcarListoDespacho(
                time=time_millis(),
                ingestion=time_millis(),
                datacontenttype=ComandoMarcarListoDespachoPayload.__name__,
                specversion="1",
                service_name="1",
                data=ComandoMarcarListoDespachoPayload(
                    id_orden=id_orden,
                    id_conductor=id_conductor,
                    direccion_entrega=direccion_entrega
                )
            )

            despachador = producer.Despachador()
            despachador.publicar_mensaje(evento, "comando-marcar-listo-despacho")

        else:
            raise Exception("No hay ningun conductor disponible, regla de negocio")

    cliente.close()


escuchar_mensaje("evento-asignar-conductor", ComandoAsignarConductor)
