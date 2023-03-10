from dataclasses import dataclass, field
from productos.seedwork.dominio.fabricas import Fabrica
from productos.seedwork.dominio.repositorios import Repositorio
from productos.modulos.dominio.entidades import Producto
from productos.modulos.dominio.repositorios import RepositorioProductos
from productos.modulos.infraestructura.repositorios import RepositorioProductosSQLAlchemy
from productos.seedwork.dominio.excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioProductos:
            return RepositorioProductosSQLAlchemy()
        else:
            raise ExcepcionFabrica(f'No existe fábrica para el objeto {obj}')
