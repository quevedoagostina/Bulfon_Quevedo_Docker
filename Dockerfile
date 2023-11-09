# Usa la imagen de Python como base
FROM python:3.9

# Establece la variable de entorno PYTHONUNBUFFERED a '1' para que Python no bufeé la salida
ENV PYTHONUNBUFFERED 1

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos de requerimientos al directorio de trabajo
COPY requirements.txt /app/

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido actual al directorio de trabajo
COPY . /app/

# Expone el puerto 5000 en el contenedor
EXPOSE 5000

# Comando a ejecutar cuando se inicie el contenedor
CMD ["./setup.sh"]
