from productos.seedwork.aplicacion.comandos import Comando
from .base import ProductoBaseHandler
from dataclasses import dataclass
from productos.seedwork.aplicacion.comandos import ejecutar_commando as comando
from productos.modulos.dominio.entidades import Producto
from pydispatch import dispatcher
from productos.modulos.infraestructura.repositorios import RepositorioProductos
from productos.config.db import db


@dataclass
class RevertirDisminuirStock(Comando):
    id_producto: str
    id_orden: str
    cantidad: int
    direccion_entrega: str
    transaction_id: str


class RevertirDisminuirStockHandler(ProductoBaseHandler):
    def handle(self, comando: RevertirDisminuirStock) -> Producto:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioProductos)
        producto: Producto = repositorio.obtener_por_id(comando.id_producto)
        producto.revertir_disminuir_stock(comando.cantidad, {
            "id_orden": comando.id_orden,
            "direccion_entrega": comando.direccion_entrega,
            "transaction_id": comando.transaction_id
        })
        repositorio.actualizar(producto)
        for evento in producto.eventos:
            dispatcher.send(signal=f'{type(evento).__name__}Integracion', evento=evento)
        db.session.commit()
        return producto


@comando.register(RevertirDisminuirStock)
def ejecutar_comando_revertir_disminuir_stock(comando: RevertirDisminuirStock) -> Producto:
    handler = RevertirDisminuirStockHandler()
    return handler.handle(comando)
