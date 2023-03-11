import threading

from saga_coreografia.consumer import escuchar_mensaje_orden_creada, escuchar_mensaje_disminuir_stock, \
    escuchar_mensaje_asignar_conductor, escuchar_mensaje_revertir_disminuir_stock, escuchar_mensaje_revertir_crear_orden

threading.Thread(target=escuchar_mensaje_orden_creada).start()
threading.Thread(target=escuchar_mensaje_disminuir_stock).start()
threading.Thread(target=escuchar_mensaje_asignar_conductor).start()
threading.Thread(target=escuchar_mensaje_revertir_disminuir_stock).start()
threading.Thread(target=escuchar_mensaje_revertir_crear_orden).start()
