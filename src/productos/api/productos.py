import json
from flask import redirect, render_template, request, session, url_for
from flask import Response, jsonify
import productos.seedwork.presentacion.api as api
from productos.seedwork.dominio.excepciones import ExcepcionDominio
from productos.modulos.aplicacion.comandos.crear_producto import CrearProducto
from productos.seedwork.aplicacion.comandos import ejecutar_commando
from productos.seedwork.aplicacion.queries import ejecutar_query
from productos.modulos.aplicacion.mapeadores import MapeadorProductoDTOJson
from productos.seedwork.aplicacion.comandos import ejecutar_commando
from productos.modulos.aplicacion.comandos.crear_producto import CrearProducto
from productos.modulos.aplicacion.queries.listar_productos import ListarProductos
from productos.modulos.aplicacion.queries.obtener_producto import ObtenerProducto
from productos.modulos.aplicacion.comandos.eliminar_producto import EliminarProducto
from productos.modulos.aplicacion.comandos.disminuir_stock import DisminuirStock
from productos.modulos.infraestructura.schema.v1.comandos import ComandoDismunirStock, ComandoDismunirStockPayload
from productos.seedwork.infraestructura import utils
from productos.modulos.infraestructura.despachadores import Despachador

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
        return jsonify({ 'mssg': 'Procesando mensaje'}), 203
    except ExcepcionDominio as e:
        return jsonify({ 'error': str(e)}), 400
    
@bp.route('/', methods=('GET',))
def index():
    try:
        query = ListarProductos()
        productos = ejecutar_query(query)
        return jsonify(productos)
    except ExcepcionDominio as e:
        return jsonify({ 'error': str(e)}), 400
    
@bp.route('/<id>', methods=('GET',))
def show(id):
    try:
        query = ObtenerProducto(id)
        producto = ejecutar_query(query)
        return jsonify(producto)
    except ExcepcionDominio as e:
        return jsonify({ 'error': str(e)}), 400
    
@bp.route('/<id>', methods=('DELETE',))
def destroy(id):
    try:
        comando = EliminarProducto(id)
        ejecutar_commando(comando)
        return jsonify({ 'mssg': 'ok'})
    except ExcepcionDominio as e:
        return jsonify({ 'error': str(e)}), 400