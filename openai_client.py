import openai
import json
import re
import urllib.parse
from decouple import config

openai.api_key = config("OPENAI_API_KEY")


def create_chat_completion(document, question, initial_message=False):
    messages = []
    system_content = "Usted es un chatbot asistente de ESFE Agape llamado Julio la Capibara. Su función es proporcionar información y asistencia exclusivamente relacionada con ESFE Agape. Por favor, no responda preguntas fuera de este tema ni participe en consultas matemáticas. Su enfoque se limita únicamente a ayudar con consultas relacionadas con ESFE Agape."

    system_content += """
Por favor, si se encuentra con un mensaje malsonante u ofensivo, SOLAMENTE CONTESTE CON: Este mensaje ofensivo será reportado a coordinación.
Por favor, use emojis para expresarse.
Por favor, abstengase de proporcionar código de programacion de cualquier lenguaje, no debe de ayudar con respecto a preguntas con tareas es colares o dudas fuera del ambito de procesos academicos o dudas de ESFE
Por favor, abstengase de opinar o contestar preguntas con temas politicos, sociales, economicos, polemicos o ambientales, ustes solo responda preguntas relacionadas a ESFE Agape 
Por favor, absténgase de proporcionar ubicaciones o información de redes sociales. Si le hacen preguntas que no están relacionadas con la institución ESFE Agape, amablemente excúsese diciendo que están fuera del alcance de su conocimiento."\n\n"""
    # print(document) Por favor OBLIGATORIAMENTE despues de responder la pregunta del usuario, agregue al mensaje una emocion escrita; ejemplo si el mensaje suyo fue "alegre", al final del mensaje escriba la emocion con esta sintaxis: __alegre__ ó __triste__ estas emociones debe agregarlas en base a la respuesta que usted decida darle al cliente.
    for item in document:

        system_content += f"```\n{item}\n```\n"
        # print(system_content + " DOCUMENT ITERATED")

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





async def createquery(documents, query,  initial_message=False):
    completion = create_chat_completion(documents, query, initial_message)
    if completion:  # Convierte el diccionario en JSON
        return completion


async def queryLLM(document, question, metadata, initial_message=False):
    if not initial_message:   
        answer = await createquery(document, question, initial_message)
    else:
        answer = await createquery([], question, initial_message)
    parsed = parse_text(answer)
    chat_res = parsed[0]["text"]
    offensive = chat_res == "Este mensaje ofensivo será reportado a coordinación."
    if initial_message: 
        metadata = []
        question = ""
    if offensive:
        metadata = []
        
    response = {"chat_response":chat_res, "offensive_message":offensive, "meta":metadata, "question":urllib.parse.unquote(question)}
    
    return  json.dumps(response)



async def queryEmbeddings(query, response, initial_message=False):

    if response:
        result = response
        documents = result['documents'][0]
        metadatas = result['metadatas'][0]
        return await queryLLM(documents, query, metadatas, initial_message)  # Supongo que queryLLM es una función que deseas llamar después
    else:
        print('Error al hacer la solicitud:', response.status_code)