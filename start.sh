#!/bin/sh

# Iniciar la aplicación Flask
gunicorn app:app -w 2 --threads 2 -b 0.0.0.0:80 &

# Ejecutar el archivo client.py
python client.py
