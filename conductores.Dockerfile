# Empezar corriendo una imagen de python
FROM --platform=linux/amd64 python:3.8-alpine

COPY ./conductores-requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./src/conductores /app

ENV MULTIPLICACION_MS localhost:8080

ENTRYPOINT [ "python" ]

CMD ["main.py" ]