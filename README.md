# poc-monoliticas
PoC para curso monoliticas


Dockerfile de pulsar
-docker pull apachepulsar/pulsar:latest --platform linux/amd64

Para correrlo:
-docker run --platform linux/amd64 -it -p 6650:6650 -p 8080:8080 apachepulsar/pulsar:latest bin/pulsar standalone 
