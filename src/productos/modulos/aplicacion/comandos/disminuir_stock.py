from productos.seedwork.aplicacion.comandos import Comando
from .base import ProductoBaseHandler
from dataclasses import dataclass
from productos.seedwork.aplicacion.comandos import ejecutar_commando as comando
from productos.modulos.aplicacion.dto import ProductoDTO
from productos.modulos.dominio.entidades import Producto
from pydispatch import dispatcher
from productos.modulos.infraestructura.repositorios import RepositorioProductos
from productos.config.db import db

@dataclass
class DisminuirStock(Comando):
    id_producto: str
    id_orden: str
    cantidad: int
    direccion_entrega: str
    transaction_id: str


class DisminuirStockHandler(ProductoBaseHandler):
    def handle(self, comando: DisminuirStock) -> Producto:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioProductos)
        producto: Producto = repositorio.obtener_por_id(comando.id_producto)
        producto.disminuir_stock(comando.cantidad, {
            "id_orden": comando.id_orden,
            "direccion_entrega": comando.direccion_entrega,
            "transaction_id": comando.transaction_id
        })
        repositorio.actualizar(producto)
        for evento in producto.eventos:
            dispatcher.send(signal=f'{type(evento).__name__}Integracion', evento=evento)
        db.session.commit()
        return producto


@comando.register(DisminuirStock)
def ejecutar_comando_disminuir_stock(comando: DisminuirStock) -> Producto:
    handler = DisminuirStockHandler()
    return handler.handle(comando)
