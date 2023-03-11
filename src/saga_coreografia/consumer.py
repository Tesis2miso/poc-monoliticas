import pulsar
from pulsar.schema import *
from utils import broker_host
from eventos import OrdenCreada, ComandoDismunirStock, ComandoAsignarConductor, ComandoRevertirDisminuirStock, ComandoRevertirOrdenCreada
from database import DbExecutor

TOPICO_ORDEN_CREADA = "evento-ordenes-2"
TOPICO_DISMINUIR_STOCK = "comando-disminuir-stock"
TOPICO_ASIGNAR_CONDUCTOR = "comando-asignar-conductor"
TOPICO_LISTO_DESPACHO = "comando-marcar-listo-despacho-2"


def escuchar_mensaje_orden_creada():
    cliente = pulsar.Client(f'pulsar://{broker_host()}:6650')
    consumer = cliente.subscribe(TOPICO_ORDEN_CREADA, schema=AvroSchema(OrdenCreada), subscription_name='evento')
    while True:
        msg = consumer.receive()
        message = msg.value()

        consumer.acknowledge(msg)
        transaction_id = message.transaction_id

        print(f"evento orden creada, transaction_id {transaction_id}")

        db = DbExecutor()
        db.insert_log(transaction_id, False, "CrearOrden", str(message))
        print("finish")

    cliente.close()


def escuchar_mensaje_disminuir_stock():
    cliente = pulsar.Client(f'pulsar://{broker_host()}:6650')
    consumer = cliente.subscribe(TOPICO_DISMINUIR_STOCK, schema=AvroSchema(ComandoDismunirStock), subscription_name='evento')
    while True:
        msg = consumer.receive()
        message = msg.value()

        consumer.acknowledge(msg)
        transaction_id = message.data.transaction_id

        print(f"evento disminuir stock, transaction_id {transaction_id}")

        db = DbExecutor()
        db.insert_log(transaction_id, False, "DisminuirStock", str(message))
        print("finish")

    cliente.close()


def escuchar_mensaje_asignar_conductor():
    cliente = pulsar.Client(f'pulsar://{broker_host()}:6650')
    consumer = cliente.subscribe(TOPICO_ASIGNAR_CONDUCTOR, schema=AvroSchema(ComandoAsignarConductor), subscription_name='evento')
    while True:
        msg = consumer.receive()
        message = msg.value()

        consumer.acknowledge(msg)
        transaction_id = message.data.transaction_id

        print(f"evento asignar conductor, transaction_id {transaction_id}")

        db = DbExecutor()
        db.insert_log(transaction_id, False, "AsignarConductor", str(message))
        print("finish")

    cliente.close()


def escuchar_mensaje_revertir_disminuir_stock():
    cliente = pulsar.Client(f'pulsar://{broker_host()}:6650')
    consumer = cliente.subscribe(TOPICO_ASIGNAR_CONDUCTOR, schema=AvroSchema(ComandoRevertirDisminuirStock), subscription_name='evento')
    while True:
        msg = consumer.receive()
        message = msg.value()

        consumer.acknowledge(msg)
        transaction_id = message.data.transaction_id

        print(f"evento revertir disminuir stock, transaction_id {transaction_id}")

        db = DbExecutor()
        db.insert_log(transaction_id, True, "DisminuirStockRevertido", str(message))
        print("finish")

    cliente.close()


def escuchar_mensaje_revertir_crear_orden():
    cliente = pulsar.Client(f'pulsar://{broker_host()}:6650')
    consumer = cliente.subscribe(TOPICO_DISMINUIR_STOCK, schema=AvroSchema(ComandoRevertirOrdenCreada), subscription_name='evento')
    while True:
        msg = consumer.receive()
        message = msg.value()

        consumer.acknowledge(msg)
        transaction_id = message.data.transaction_id

        print(f"evento revertir crear orden, transaction_id {transaction_id}")

        db = DbExecutor()
        db.insert_log(transaction_id, True, "CrearOrdenRevertido", str(message))
        print("finish")

    cliente.close()
