from productos.seedwork.aplicacion.comandos import ComandoHandler
from productos.modulos.infraestructura.fabricas import FabricaRepositorio
from productos.modulos.dominio.fabricas import FabricaProductos

class CrearProductoBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_productos: FabricaProductos = FabricaProductos()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_productos(self):
        return self._fabrica_productos    
    