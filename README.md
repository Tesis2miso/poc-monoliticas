# poc-monoliticas
PoC para curso monoliticas

Dockerfile de pulsar
-docker pull apachepulsar/pulsar:latest --platform linux/amd64

Para correrlo:
-docker run --platform linux/amd64 -it -p 6650:6650 -p 8080:8080 apachepulsar/pulsar:latest bin/pulsar standalone 

## Crear ambiente con conda

```bash
conda create --name monoliticas
```

## Usar ambiente con conda

```bash
conda activate monoliticas
```

## Instalar dependencias

```bash
pip install -r requirements.txt
```

## Iniciar microservicio productos

Desde el directorio principal ejecute el siguiente comando.

```bash
flask --app src/productos/api run
```

Siempre puede ejecutarlo en modo DEBUG:

```bash
flask --app src/productos/api --debug run
```

## Correr pulsar

```bash
export DOCKER_DEFAULT_PLATFORM=linux/amd64
docker-compose --profile pulsar up
```

## Correr db

```bash
export DOCKER_DEFAULT_PLATFORM=linux/amd64
docker-compose --profile db up
```

## Parar pulsar

```bash
docker-compose --profile pulsar stop
```

## Parar db

```bash
docker-compose --profile db stop
```

### Kill proceso que esta usando un puerto
```bash
fuser -k <puerto>/tcp
```
