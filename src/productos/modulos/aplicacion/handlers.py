from productos.modulos.dominio.eventos.productos import StockDisminuido
from productos.seedwork.aplicacion.handlers import Handler
from productos.modulos.infraestructura.despachadores import Despachador
from productos.modulos.infraestructura.schema.v1.comandos import ComandoAsignarConductor, \
    ComandoAsignarConductorPayload, ComandoRevertirOrdenCreada, ComandoRevertirOrdenCreadaPayload
from productos.seedwork.infraestructura import utils
from productos.config.config import Config

class HandlerProductoIntegracion(Handler):

    @staticmethod
    def handle_stock_disminuido(evento):
        despachador = Despachador()
        evento = ComandoAsignarConductor(
            time=utils.time_millis(),
            ingestion=utils.time_millis(),
            datacontenttype=ComandoAsignarConductorPayload.__name__,
            specversion=Config.SPEC_VERSION,
            service_name=Config.SERVICE_NAME,
            data = ComandoAsignarConductorPayload(
                id_producto=str(evento.id_producto),
                id_orden=str(evento.id_orden),
                cantidad=evento.cantidad,
                direccion_entrega=evento.direccion_entrega,
                transaction_id=evento.transaction_id
            )
        )
        despachador.publicar_mensaje(evento, "comando-asignar-conductor")

    @staticmethod
    def handle_revertir_orden_creada(evento):
        despachador = Despachador()
        evento = ComandoRevertirOrdenCreada(
            time=utils.time_millis(),
            ingestion=utils.time_millis(),
            datacontenttype=ComandoRevertirOrdenCreadaPayload.__name__,
            specversion=Config.SPEC_VERSION,
            service_name=Config.SERVICE_NAME,
            data=ComandoRevertirOrdenCreadaPayload(
                id_producto=str(evento.id_producto),
                id_orden=str(evento.id_orden),
                transaction_id=evento.transaction_id
            )
        )
        despachador.publicar_mensaje(evento, "comando-revertir-orden-creada")
