import pulsar
from pulsar.schema import *
import uuid
from utils import broker_host, time_millis
from eventos import OrdenCreada, ComandoDismunirStockPayload, ComandoDismunirStock, ComandoMarcarListoDespachoPayload, ComandoMarcarListoDespacho, ComandoRevertirOrdenCreada
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
        transaction_id = message.transaction_id

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
                direccion_entrega=direccion_entrega,
                transaction_id=transaction_id
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
        transaction_id = message.data.transaction_id

        print(f"consumed message driver {id_conductor}")

        db = DbExecutor()
        db.update_order_status(id_orden, id_conductor)


        db_replica = DbExecutorReplica()
        db_replica.update_order_status(id_orden, id_conductor)

        print("finish")

    cliente.close()


def escuchar_mensaje_revertir_orden_creada(topico, schema=Record):
    cliente = pulsar.Client(f'pulsar://{broker_host()}:6650')
    consumer = cliente.subscribe(topico, schema=AvroSchema(schema), subscription_name='evento')
    while True:
        msg = consumer.receive()
        message = msg.value()

        consumer.acknowledge(msg)

        id_orden = message.data.id_orden
        id_producto = message.data.id_producto

        print(f"revertir orden creada {id_orden} and product {id_producto}")

        db = DbExecutor()
        db.update_order_status_failed(id_orden)


        db_replica = DbExecutorReplica()
        db_replica.update_order_status_failed(id_orden)

        print("finish")

    cliente.close()


threading.Thread(target=escuchar_mensaje, args=[topico, OrdenCreada]).start()
threading.Thread(target=escuchar_mensaje_revertir_orden_creada, args=["comando-revertir-orden-creada", ComandoRevertirOrdenCreada]).start()

escuchar_mensaje_conductores("comando-marcar-listo-despacho-2", ComandoMarcarListoDespacho)
