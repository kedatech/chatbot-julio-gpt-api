# Utiliza una imagen base de Python 3.12
FROM python:3.11.5

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de la aplicación a la imagen
COPY . /app

# Actualiza pip y luego instala las dependencias de la aplicación
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Expone el puerto en el que se ejecutará la aplicación Flask
# EXPOSE 80

# Inicia la aplicación Flask cuando se inicia el contenedor
# CMD ["gunicorn ","--bind","0.0.0.0:80", "app:app"]

# ENTRYPOINT ["./gunicorn.sh"]
CMD ["./start.sh"]
