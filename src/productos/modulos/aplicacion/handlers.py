from productos.modulos.dominio.eventos.productos import StockDisminuido
from productos.seedwork.aplicacion.handlers import Handler
from productos.modulos.infraestructura.despachadores import Despachador

class HandlerProductoIntegracion(Handler):

    @staticmethod
    def handle_stock_disminuido(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-productos')
