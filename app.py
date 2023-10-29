import os
import json

from flask import Flask, request, jsonify
from flask_cors import CORS
from openai_client import queryEmbeddings, create_chat_completion
from process import process_files, query_collection, speechTotext

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return "This is the index try with: /query or /train"

@app.route('/train', methods=['GET'])
def train():
    archivos = getDocumets()
    process_files(archivos)
    response = "IA entrenada correctamente."
    return jsonify(response)


@app.route('/init', methods=['GET'])
async def initial_message():
    query = "Hola"
    collections = query_collection(query)
    response = await queryEmbeddings(query, collections, True)

    return jsonify(json.loads(response))

@app.route('/query', methods=['GET'])
async def query():
    query = request.args.get('text')
    collections = query_collection(query)
    response = await queryEmbeddings(query, collections)

    return jsonify(json.loads(response))


@app.route("/speech", methods=['GET'])
async def speech():
    return "This is a construct request 🔨"
    # query = request.args.get('text')
    # collections = query_collection(query)
    # response = await queryEmbeddings(query, collections)

    # return jsonify(json.loads(response))

if __name__ == '__main__':
    app.run(host="0.0.0.0")

def getDocumets():
    carpeta_archivos = 'Markdowns/'
    archivos = []
    nombres_archivos = os.listdir(carpeta_archivos)

    # Recorre la lista de nombres de archivos y abre cada archivo
    for nombre_archivo in nombres_archivos:
        ruta_archivo = os.path.join(carpeta_archivos, nombre_archivo)

        # Verifica si es un archivo (no un directorio) antes de abrirlo
        if os.path.isfile(ruta_archivo):
            with open(ruta_archivo, 'r') as archivo:
                contenido = archivo.read()
                archivos.append({'filename': nombre_archivo, 'content': contenido})

    return archivos
