# PoC monoliticas

PoC para curso monoliticas

## Integrantes

- Andres Baron
- Emilson Quintero
- Laura Bello
- William Ravelo

## Arquitectura

En el siguiente diagrama se puede ver los componentes y topicos principales al igual que su interacción.

![Base monoliticas drawio (1)](https://user-images.githubusercontent.com/16025512/222797394-c0005067-1ea4-4c8e-8f3d-bddefd65a9f3.png)

De igual forma el siguiente diagrama presenta a nivel de componentes como fueron desplegados

![Base monoliticas drawio (2)](https://user-images.githubusercontent.com/16025512/222797509-9463e90c-7b79-4334-8a1f-b96f05d5a8dd.png)

## DDD

En este diagrama se pueden ver los contextos acotados implementados junto con sus dominios

![Base monoliticas drawio](https://user-images.githubusercontent.com/16025512/222797116-9794b27a-7f93-4699-9163-bfe2f449a1ed.png)

## Escenarios de calidad a probar

- [Escenario calidad #3 (Modificabilidad)](https://github.com/Tesis2miso/poc-monoliticas/wiki/Escenario-calidad-%233-(Modificabilidad))
- [Escenario calidad #6 (Escalabilidad)](https://github.com/Tesis2miso/poc-monoliticas/wiki/Escenario-calidad-%236-(Escalabilidad))
- [Escenario calidad #8 (Disponibilidad)](https://github.com/Tesis2miso/poc-monoliticas/wiki/Escenario-calidad-%238-(Disponibilidad))

## Justificaciones

##### Se justifica correctamente los tipos de eventos a utilizar (integración o carga de estado). Ello incluye la definición de los esquemas y evolución de los mismos.

Para el flujo de creación de órdenes y productos usamos una arquitectura basada en eventos tanto desde el BFF como en la interacción de todos los componentes por medio de una coreografia. En esta interacción usamos eventos de integración para todos los componentes y eventos de dominio para realizar proyecciones en la base de datos del componente de productos. Inicialmente usamos eventos de integración ya que necesitamos comunicar componentes que hacen parte de dominios diferentes y porque los datos a enviar por la cola de mensajes son limitados no son todos los de la orden si no los que se necesitan para cumplir con la serie de comandos a ejecutar, esto dado que no estamos duplicando información en la base de datos a excepción de los datos que se encuentran en los eventos. De igual forma, los eventos de dominio se usaron para notificar dentro del dominio de productos cuando sucedió una acción y asi permitir dispatchers escuchar estos eventos y que puedan realizar la proyección correspondiente en la base de datos dedicada a solo lectura promoviendo CQRS.

En cuanto a la definición y evolución de esquemas hicimos uso de AVRO que obliga a que los microservicios tengan que cumplir con el esquema propuesto y en caso de no hacerlo no permite el envio de los mensajes ya que se lanza un error de schema incompatible. Apache Pulsar nos ayuda con su schema registry para poder hacer registro de cada uno de los schema de los mensajes, finalmente se cuenta con un specversion dentro de cada evento indicando la versión del schema, para que en caso de querer lanzar una nueva versión solo sea necesario registrar un nuevo schema.

A continuación se presenta un ejemplo de una definición de un schema utilizado en los componentes.

```python
class ComandoAsignarConductorPayload(ComandoIntegracion):
    id_producto = String()
    id_orden = String()
    cantidad = Integer()
    direccion_entrega = String()

class ComandoAsignarConductor(ComandoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = ComandoAsignarConductorPayload()
```

##### Justificó e implementó alguna de las topologías para la administración de dato

Justificacion

## Descripción de actividades

- **Andres Baron**: Realizó el componente de ordenes junto con su implementación de almacenamiento, conexión y uso de la cola de mensajes, de igual forma configuración de Apache Pulsar en la nube.
- **Emilson Quintero**: Realizó el componente de BFF junto con su conexión y uso de cola de mensajes al igual que implementación necesaria para cumplir con escenario de calidad #3.
- **Laura Bello**: Realizó el componente de conductores junto con su implementación de almacenamiento, conexión y uso de la cola de mensajes.
- **William Ravelo M**: Realizó el componente de productos junto con su implementación de almacenamiento, conexión y uso de la cola de mensajes.
- **Todos**: Integración y pruebas de todos los componentes al igual que el flujo de creación de ordenes y su confirmación. De igual forma, despliegue de todos los componentes en la nube para luego su documentación y pruebas de escenarios de calidad.

## Requisitos

- Python 3
- Apache pulsar

## Pulsar desde dockerfile

Dockerfile de pulsar

```bash
docker pull apachepulsar/pulsar:latest --platform linux/amd64
```

Para correrlo:

```bash
docker run --platform linux/amd64 -it -p 6650:6650 -p 8080:8080 apachepulsar/pulsar:latest bin/pulsar standalone 
```

### Tmux

Para desplegar y tener multiples sesiones se uso tmux, estos son algunos comandos frecuentes

- Crear nueva sesion con nombre

```bash
tmux new -s <NAME>
```

- Conectarse a sesion

```bash
tmux attach-session -t <NAME>
```

- Desconectarse de sesion

```bash
tmux detach -s <NAME>
```

- Listar sesiones

```bash
tmux ls
```

- Renombrar ventana

```bash
tmux rename-window '<NAME>'
```

### Variables de entorno

Se necesitan las siguientes variables de entorno

```bash
export DB_USERNAME=
export DB_PASSWORD=
export DB_HOSTNAME=
export DB_NAME=
export BROKER_HOST=
export DB_READ_NAME=
export DB_READ_HOSTNAME=
```

### Crear ambiente con conda

```bash
conda create --name monoliticas
```

### Usar ambiente con conda

```bash
conda activate monoliticas
```

### Instalar dependencias

```bash
pip install -r requirements.txt
pip install -r conductores-requirements.txt
```

## Microservicio BFF

Desde el directorio principal ejecute el siguiente comando.

```bash
flask --app src/bff  run
python3 -m flask --app src/bff  run --host=0.0.0.0 -p 3000
```

## Microservicio ordenes

Desde el directorio principal ejecute el siguiente comando.

```bash
python3 src/ordenes/consumer.py
```

## Microservicio productos

Desde el directorio principal ejecute el siguiente comando.

```bash
flask --app src/productos/api run
python3 -m flask --app src/productos/api run --host=0.0.0.0 -p 3001
```

## Microservicio conductores

Desde el directorio principal ejecute el siguiente comando.

```bash
python3 src/conductores/consumer.py
```

## Utils
### Correr pulsar

```bash
export DOCKER_DEFAULT_PLATFORM=linux/amd64
docker-compose --profile pulsar up
```

### Correr db

```bash
export DOCKER_DEFAULT_PLATFORM=linux/amd64
docker-compose --profile db up
```

### Parar pulsar

```bash
docker-compose --profile pulsar stop
```

### Parar db

```bash
docker-compose --profile db stop
```

### Consumer tester

```bash
python ./testers/consumer_tester.py
```

### Producer tester

```bash
python ./testers/producer_tester.py
```
