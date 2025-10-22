#!/usr/bin/env bash
# start.sh

# Render usará este script para iniciar la API.
# Instala las librerías necesarias para el servidor de producción (Gunicorn y Uvicorn workers).
pip install gunicorn uvicorn

# Inicia la aplicación. $PORT es una variable de entorno proporcionada por Render.
gunicorn src.app:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT