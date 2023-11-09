#!/bin/bash

# Clonar el repositorio (opcional si ya está clonado)
# git clone git@github.com:quevedoagostina/Bulfon_Quevedo_MiniBlog.git
# cd Bulfon_Quevedo_MiniBlog

# Crear y activar el entorno virtual (asegúrate de tener el entorno virtual ya creado)
# source tu_entorno/bin/activate

# Instalar las dependencias
pip install -r requirements.txt

# Crear migraciones iniciales
flask db init

# Realizar los cambios necesarios
flask db migrate -m "..."

# Aplicar las migraciones a la base de datos
flask db upgrade

# Iniciar la aplicación
flask run --host=0.0.0.0
