#imagen python.
FROM python:3.9-alpine

# Copia el directorio del contenedor.
COPY . /sql_alchemy
WORKDIR /sql_alchemy

RUN apk update \
    && apk add --no-cache bash build-base

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Define environment variables
ENV FLASK_APP=app.app:app
ENV FLASK_RUN_HOST=0.0.0.0

# CMD ["flask", "run", "--host=0.0.0.0", "--port=5005"] # Comentado para ejecutar gunicorn

CMD ["sh", "run.sh"]
