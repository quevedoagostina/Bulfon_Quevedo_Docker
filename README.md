# Miniblog con Python Flask y Docker

Este miniblog permite a los usuarios crear y compartir sus propios posteos. Utiliza Python con Flask y una base de datos MySQL.

## Requisitos

- Docker (última versión)
- Git

## Configuración

1. Clona este repositorio:


2. Asegúrate de tener el archivo `.env` con la configuración necesaria para la aplicación Flask y la base de datos MySQL. Puedes basarte en el archivo `.env.example` proporcionado.

3. Asegúrate de tener Docker instalado y funcionando en tu máquina.

## Uso

1. Ejecuta Docker Compose para construir y levantar los contenedores:

    ```bash
    docker-compose up --build
    ```

    Esto construirá las imágenes y pondrá en marcha los contenedores definidos en el archivo `docker-compose.yml`.

2. Después de la ejecución, la aplicación estará disponible en [http://localhost:5000](http://localhost:5000).

## Notas importantes

- No es necesario configurar el entorno virtual o instalar dependencias manualmente, ya que se ejecutan en los contenedores Docker.
- Las migraciones de la base de datos se realizan automáticamente con las configuraciones proporcionadas en el archivo `docker-compose.yml`.
- Se proporciona una script `app/init_db.py` para agregar las categorías a la base de datos. Puedes ejecutarlo utilizando:

    ```bash
    docker-compose run web python init_db.py
    ```

    Asegúrate de que los contenedores estén en funcionamiento antes de ejecutar este comando.

