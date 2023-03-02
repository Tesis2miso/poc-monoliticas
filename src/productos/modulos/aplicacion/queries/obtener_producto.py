from dataclasses import dataclass
from productos.modulos.dominio.entidades import Producto
from productos.modulos.infraestructura.repositorios import RepositorioProductos
from productos.seedwork.aplicacion.queries import Query, QueryResultado
from productos.seedwork.aplicacion.queries import ejecutar_query as query
from .base import ProductoQueryBaseHandler

@dataclass
class ObtenerProducto(Query):
    id: str

class ObtenerProductoHandler(ProductoQueryBaseHandler):

    def handle(self, query: ObtenerProducto) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioProductos)
        producto: Producto = repositorio.obtener_por_id(query.id)
        return QueryResultado(resultado=producto)

@query.register(ObtenerProducto)
def ejecutar_query_obtener_producto(query: ObtenerProducto):
    handler = ObtenerProductoHandler()
    return handler.handle(query)