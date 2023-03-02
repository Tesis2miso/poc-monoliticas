from .entidades import Producto
from .reglas import StockNoPuedeSerNegativo
from .excepciones import TipoObjetoNoExisteEnDominioInventarioExcepcion
from productos.seedwork.dominio.repositorios import Mapeador, Repositorio
from productos.seedwork.dominio.fabricas import Fabrica
from productos.seedwork.dominio.entidades import Entidad
from productos.seedwork.dominio.eventos import EventoDominio
from dataclasses import dataclass

@dataclass
class _FabricaProducto(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad) or isinstance(obj, EventoDominio):
            return mapeador.entidad_a_dto(obj)
        else:
            producto: Producto = mapeador.dto_a_entidad(obj)
            self.validar_regla(StockNoPuedeSerNegativo(producto))
            return producto
        
@dataclass
class FabricaProductos(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Producto.__class__:
            fabrica_producto = _FabricaProducto()
            return fabrica_producto.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioInventarioExcepcion()