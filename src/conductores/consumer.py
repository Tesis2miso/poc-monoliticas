import pulsar
from pulsar.schema import *
from utils import broker_host
from eventos import ComandoAsignarConductor, ComandoMarcarListoDespacho, ComandoMarcarListoDespachoPayload, ComandoRevertirDisminuirStock, ComandoRevertirDisminuirStockPayload
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

        print(f'Llego mensaje {message}')
        id_orden = message.data.id_orden
        direccion_entrega = message.data.direccion_entrega
        transaction_id = message.data.transaction_id
        id_producto = message.data.id_producto
        cantidad = message.data.cantidad

        db = DbExecutor()

        id_conductor = None
        if len(db.get_unassigned_conductor()) > 0:
            id_conductor = db.get_unassigned_conductor()[0]

        print(f"el id del conductor es {id_conductor}")

        if id_conductor:
            print('Asignando conductor')
            db.assign_conductor(id_conductor, id_orden, direccion_entrega)
            print('Conductor asignado')

            evento = ComandoMarcarListoDespacho(
                time=time_millis(),
                ingestion=time_millis(),
                datacontenttype=ComandoMarcarListoDespachoPayload.__name__,
                specversion="2",
                service_name="2",
                data=ComandoMarcarListoDespachoPayload(
                    id_orden=id_orden,
                    id_conductor=str(id_conductor),
                    direccion_entrega=direccion_entrega,
                    transaction_id=transaction_id
                )
            )

            despachador = producer.Despachador()
            despachador.publicar_mensaje(evento, "comando-marcar-listo-despacho-2")

            print('Despachar enviado!')

        else:
            evento = ComandoRevertirDisminuirStock(
                time=time_millis(),
                ingestion=time_millis(),
                datacontenttype=ComandoRevertirDisminuirStockPayload.__name__,
                specversion="2",
                service_name="2",
                data=ComandoRevertirDisminuirStockPayload(
                    id_orden=id_orden,
                    id_producto=str(id_producto),
                    cantidad=cantidad,
                    direccion_entrega=direccion_entrega,
                    transaction_id=transaction_id
                )
            )

            despachador = producer.Despachador()
            despachador.publicar_mensaje(evento, "comando-revertir-disminuir-stock")

            print("No hay ningun conductor disponible, regla de negocio")

    cliente.close()


escuchar_mensaje("comando-asignar-conductor", ComandoAsignarConductor)
