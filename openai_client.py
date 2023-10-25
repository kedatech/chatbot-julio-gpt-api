import openai
import json
import re
import urllib.parse
from decouple import config

openai.api_key = config("OPENAI_API_KEY")


def create_chat_completion(document, question):
    messages = []

    system_content = """
Usted es un bot asistente en español latino para ESFE Agape. Su función es proporcionar información y asistencia exclusivamente relacionada con ESFE Agape. Por favor, no responda preguntas fuera de este tema ni participe en consultas matemáticas. Su enfoque se limita únicamente a ayudar con consultas relacionadas con ESFE Agape.

Soy [Tu Nombre], el asistente de ESFE Agape. Cada respuesta que ofrezca será en nombre de "Soy Julio la capibara, el asistente de ESFE Agape" en el primer mensaje.

Si se encuentra con respuestas ofensivas, por favor, informe al usuario que es un asistente de ESFE y puede informar sobre tales mensajes.

puedes usar emojis si es necesario

Por favor, absténgase de proporcionar ubicaciones o información de redes sociales. Si le hacen preguntas que no están relacionadas con la institución ESFE Agape, amablemente excúsese diciendo que están fuera del alcance de su conocimiento."\n\n"""

    print(document)
    for item in document:

        system_content += f"```\n{item}\n```\n"
        print(system_content + " DOCUMENT ITERATED")

    system_content += """
    Please provide detailed instructions on how the AI should
    interact with users, what information it should provide, and
    how it should handle various scenarios, ensuring a friendly and professional communication style.
    Consider the following points. Only just response questions of the information provided. All offensives, Theme Off,
    no help need questions, ignore them.
    """

    messages.append({"role": "system", "content": system_content})

    prompt = question

    messages.append({"role": "user", "content": prompt})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=1,
            max_tokens=1000
        )

        if response.choices and len(response.choices) > 0:
            return response.choices[0].message["content"]
        else:
            return None
    except Exception as error:
        print(error)
        return None



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
    parsed = parse_text(answer)
    response = {"chat_response":parsed[0]["text"], "meta":metadata, "question":urllib.parse.unquote(question)}
    return  json.dumps(response)



async def queryEmbeddings(query, response):

    if response:
        result = response
        documents = result['documents'][0]
        metadatas = result['metadatas'][0]
        return await queryLLM(documents, query, metadatas)  # Supongo que queryLLM es una función que deseas llamar después
    else:
        print('Error al hacer la solicitud:', response.status_code)