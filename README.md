# ChatBot Julio-GPT
Esta es una API de chatbot para Julio_GPT hecha con Python usando el micro-framework Flask

# Uso

## Entorno Virtual Python
Crea un entorno virtual en python >= 3.12 con:
```cmd
python -m venv venv
```
O crea un entorno virtual en python <= 3.11 con:
```cmd
python -m virtualenv venv
```
O crea un entorno virtual con una version de python específica:
```cmd
python -m virtualenv -p ubicacion/exe/python venv
```
Activa el entorno virtual
```cmd
venv/Scripts/activate
```
Puedes desactivarlo con
```cmd
deactivate
```

## Dependencias
Instala las dependencias
```cmd
python install -r requirements.txt
```
Crea un archivo llamado <code>.env</code> y agrega estas variables
```cmd
PORT -> es el puerto de la app, docker: 80/Flask: 5000
LOCAL_URL -> es el host local: docker: '0.0.0.0'/ Flask: '127.0.0.1'
OPENAI_API_KEY -> es tu Token de OpenAI API
```
Ahora sube tus archivos Markdown con el que entrenaremos a la IA en la carpeta <code>Markdowns</code>

## Inicializar API
En tu consola ejecuta
```cmd
flask --app app.py --debug run
```

Entrena la IA enviando una petición <code>GET</code> a <code>/train</code>

Si has subido los archivos Markdown y las dependencias están correctas recibirás esta respuesta
```json
"IA entrenada correctamente."
```

Ahora puedes hacer una petición <code>GET</code> a <code>/query?text=</code> para interactuar con la IA, debes mandar tu pregunta o query por <code>params</code>

Algo como esto
```url
localhost:5000/query?text=hola mundo
```

Si todo está bien recibirás como respuesta un formato como este
```json
{
  "chat_response": "¡Hola!",
  "meta": [
    {
      "document_title": "titulo-1",
      "file_name": "documento1.md"
    },
    {
      "document_title": "titulo-3",
      "file_name": "documento2.md"
    }
  ],
  "offensive_message": false,
  "question": "hola mundo"
}
```
Y eso es todo!

# Endpoints

## /init [GET]
Este endpoint es para inciar un nuevo chat, a diferencia de ```/query``` en este endpoint la IA saludará y dará una breve introducción como su nombre y sus servicios

### Respuesta
```json
{
  "chat_response": "¡Hola! Soy Julio la Capibara, el asistente de ESFE Agape. ¿En qué puedo ayudarte hoy? 😊",
  "meta": [],
  "offensive_message": false,
  "question": ""
}
```
## /train [GET]
Este endpoint entrenará a la IA en base a los archivos Markdowns proporcionados, si la carpeta está vacía, la IA no tendrá ningun recurso al que acudir y solo funcionará la pura IA de Openai
### Respuesta
```json
"IA entrenada correctamente"
```

## /query?text= [GET]
Este endpoint es para interactuar con la IA y hacerle consultas con respecto a cualquier tema relacionado al entrenamiento. La pregunta se debe enviar por params.

### Respuesta
```json
{
  "chat_response": "¡Hola! El precio para la apertura del servicio social es de $5, a menos que seas becado. ¿Hay algo más en lo que pueda ayudarte? 😊",
  "meta": [
    {
      "document_title": "Todo sobre el servicio social",
      "file_name": "ch1-servicio-social.md"
    }
  ],
  "offensive_message": false,
  "question": "¿Hola, sabes el precio del servicio social?"
}
```

En caso de que el texto que se haya enviado sea ofensivo, la IA lo hará saber con la siguiente respuesta
```json
{
  "chat_response": "Este mensaje ofensivo será reportado a coordinación.",
  "meta": [],
  "offensive_message": true,
  "question": "idiota"
}
```

# Sobre el Proyecto

## Descripción general
El proyecto se realiza con Flask, el proyecto es una API simple que se comunica con dos servicios: OpenAI y ChromaDb.
ChromaDB sirve como una base de datos vectorial y, por lo tanto, crea incrustaciones o embeddings, lo cual es costoso en términos de tokens o el uso se refiere a la API OpenAI, en cambio, OpenAI se usa junto con el proyecto para responder de manera sensata y condicional con la capacitación indicada

## Entrenamiento
El entrenamiento se basa en el uso de archivos Markdown con el contenido que desea entrenar, pueden ser elementos de cocina o el tema deseado, la IA lo entenderá y entrenará

La IA buscará clasificar los archivos por el tema principal o h1 de los Markdowns, que es "#", por lo que su tema debe ser conciso y claro para que la IA sea más fácil de guardar y buscar ese tema

La IA separará cada tema o sección (incrustación) por un subtema o un "###", a partir de ahí, la IA tomará el texto anterior como una sección o tema separado y tomará el nuevo como una nueva sección o tema. Por ejemplo :
```md
# Métodos para centrar un div
blablablabla
### -> SEPARACION

# Cómo importar esto a JS -> Nuevo Tema
blablabla.
```

# Resursos a los que acudir

<strong>Flask</strong>: <https://flask.palletsprojects.com/en/3.0.x/>  <br>
<strong>ChromaDB</strong>: <https://docs.trychroma.com/> <br>
<strong>OpenAI</strong>: <https://platform.openai.com/> <br>

# TO-DO
## 1. Refactorizar el código ♻️
## 2. Añadir a .env una variable ```OPENAI_PROMPT``` para que sea más sencillo modificar el condicionamiento de la IA 🔨
## 3. Implementar dictado por audios 🤖
## 4. Permitir que la IA proporcione recursos como Links, Imágenes o artículos de utilidad 📖

