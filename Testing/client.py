from openai_client import create_chat_completion
import requests
from env import BACKEND_SERVER  # Asegúrate de que esta variable contenga la URL correcta
import asyncio
import re

class TextBlock:
    def __init__(self, isCodeBlock, text, language=None):
        self.isCodeBlock = isCodeBlock
        self.text = text
        self.language = language

def parse_text(text)->TextBlock:
    regex = r'```([\w-]+)?\s*([\s\S]+?)\s*```'
    blocks:TextBlock = []
    last_index = 0

    for match in re.finditer(regex, text):
        full_match, language, code = match.groups()
        pre_match = text[last_index:match.start()]

        if pre_match:
            blocks.append({'isCodeBlock': False, 'text': pre_match})

        blocks.append({'isCodeBlock': True, 'text': code, 'language': language})
        last_index = match.end()

    last_block = text[last_index:]

    if last_block:
        blocks.append({'isCodeBlock': False, 'text': last_block})

    return blocks





async def createquery(d, q):
    completion = create_chat_completion(d, q)
    if completion:  # Convierte el diccionario en JSON
        return completion


async def queryLLM(document, question, metadata):
    answer = await createquery(document, question)
    # print(answer)
    parsed = parse_text(answer)
    response = {"text":parsed[0]["text"], "meta":metadata}
    return  response





async def queryEmbeddings():
    query = "que pasa si no hago horas sociales?"  # Reemplaza con tu pregunta
    url = f'{BACKEND_SERVER}/query?text={query}'
    response = await asyncio.to_thread(lambda: requests.get(url, headers={'Content-Type': 'application/json'}))
    if response.status_code == 200:
        result = response.json()
        documents = result['documents'][0]
        metadatas = result['metadatas'][0]
        return await queryLLM(documents, query, metadatas)  # Supongo que queryLLM es una función que deseas llamar después
    else:
        print('Error al hacer la solicitud:', response.status_code)

# # Llama a la función queryEmbeddings
# mensaje = asyncio.run(queryEmbeddings())


# print(mensaje)


# Verifica la respuesta
# if response.status_code == 200:
#     results = response.json()
#     print('Respuesta del servidor:', results)
# else:
#     print('Error al hacer la solicitud:', response.status_code)
