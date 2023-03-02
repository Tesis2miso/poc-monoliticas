from dataclasses import dataclass
from productos.modulos.dominio.entidades import Producto
from productos.modulos.infraestructura.repositorios import RepositorioProductos
from productos.modulos.dominio.entidades import Producto
from productos.modulos.infraestructura.repositorios import RepositorioProductos
from productos.seedwork.aplicacion.queries import Query, QueryResultado
from productos.seedwork.aplicacion.queries import ejecutar_query as query
from .base import ProductoQueryBaseHandler

@dataclass
class ListarProductos(Query):
  ...

class ListarProductosHandler(ProductoQueryBaseHandler):            
    def handle(self, query: ListarProductos) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioProductos)
        productos: list[Producto] = repositorio.obtener_todos()
        return QueryResultado(resultado=productos)

@query.register(ListarProductos)
def ejecutar_query_obtener_producto(query: ListarProductos):
    handler = ListarProductosHandler()
    return handler.handle(query)
