import json
from flask import redirect, render_template, request, session, url_for
from flask import Response
import productos.seedwork.presentacion.api as api
from productos.seedwork.dominio.excepciones import ExcepcionDominio
from productos.modulos.aplicacion.comandos.crear_producto import CrearProducto
from productos.seedwork.aplicacion.comandos import ejecutar_commando
from productos.seedwork.aplicacion.queries import ejecutar_query
from productos.modulos.aplicacion.mapeadores import MapeadorProductoDTOJson
from productos.seedwork.aplicacion.comandos import ejecutar_commando
from productos.modulos.aplicacion.comandos.crear_producto import CrearProducto

bp = api.crear_blueprint('productos', '/productos')

@bp.route('/', methods=('POST',))
def crear_producto_comando():
    try:
        session['uow_metodo'] = 'pulsar'
        map_reserva = MapeadorProductoDTOJson()
        producto_dict = request.json
        producto_dto = map_reserva.externo_a_dto(producto_dict)
        comando = CrearProducto(
            producto_dto.fecha_creacion,
            producto_dto.fecha_actualizacion,
            producto_dto.id,
            producto_dto.nombre,
            producto_dto.stock
        )
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')