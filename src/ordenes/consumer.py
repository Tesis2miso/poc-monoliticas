import pulsar
from pulsar.schema import *
import uuid
from utils import broker_host, time_millis
from eventos import OrdenCreada, ComandoDismunirStockPayload, ComandoDismunirStock, ComandoMarcarListoDespachoPayload, ComandoMarcarListoDespacho
from database import DbExecutor, DbExecutorReplica
from datetime import datetime
import threading
import producer

topico = "evento-ordenes-2"


def escuchar_mensaje(topico, schema=Record):
    cliente = pulsar.Client(f'pulsar://{broker_host()}:6650')
    consumer = cliente.subscribe(topico, schema=AvroSchema(schema), subscription_name='evento')
    while True:
        msg = consumer.receive()
        message = msg.value()

        consumer.acknowledge(msg)

        id_producto = message.id_producto
        user_id = message.user_id
        cantidad = message.cantidad
        direccion_entrega = message.direccion_entrega

        print(f"consumed message {id_producto}")

        db = DbExecutor()
        order_id = str(uuid.uuid4())
        db.create_order(order_id, id_producto, user_id, cantidad, direccion_entrega)


        db_replica = DbExecutorReplica()
        db_replica.create_order(str(uuid.uuid4()), id_producto, user_id, cantidad, direccion_entrega)

        # orden = OrdenCreada(id_orden = 1, id_producto = id_producto, user_id= user_id, time_stamp = str(datetime.now()), cantidad= cantidad, direccion_entrega= direccion_entrega)

        evento = ComandoDismunirStock(
            time=time_millis(),
            ingestion=time_millis(),
            datacontenttype=ComandoDismunirStockPayload.__name__,
            specversion="1",
            service_name="1",
            data=ComandoDismunirStockPayload(
                id_producto=id_producto,
                id_orden=order_id,
                cantidad=cantidad,
                direccion_entrega=direccion_entrega
            )
        )

        print("voy a mandar", evento)

        despachador = producer.Despachador()
        despachador.publicar_mensaje(evento, "comando-disminuir-stock")

    cliente.close()


def escuchar_mensaje_conductores(topico, schema=Record):
    cliente = pulsar.Client(f'pulsar://{broker_host()}:6650')
    consumer = cliente.subscribe(topico, schema=AvroSchema(schema), subscription_name='evento')
    while True:
        msg = consumer.receive()
        message = msg.value()

        consumer.acknowledge(msg)

        id_orden = message.data.id_orden
        id_conductor = message.data.id_conductor
        direccion_entrega = message.data.direccion_entrega

        print(f"consumed message driver {id_conductor}")

        db = DbExecutor()
        db.update_order_status(id_orden, id_conductor)


        db_replica = DbExecutorReplica()
        db_replica.update_order_status(id_orden, id_conductor)

        print("finish")

    cliente.close()



threading.Thread(target=escuchar_mensaje, args=[topico, OrdenCreada]).start()

escuchar_mensaje_conductores("comando-marcar-listo-despacho-2", ComandoMarcarListoDespacho)