# chatbot-julio-gpt-api
This is a chatbot API for Julio_GPT made with Python using the Flask framework

# Use

1. Initialize your virtual environment
2. Install the dependencies in the requirements.txt file
3. in the <code>env.py</code> file enter your <code>OPENAI_API_KEY</code> from the OpenAI key and the url of your Flask server in <code>BACKEND_SERVER</code>
5. Upload your Markdown files with which you will train your AI into the <code>Markdowns</code> directory, the AI will take the first topic "#" as a reference and finish that section (embbeding) with "###" so classify your sections or themes well
4. Train AI by request to <code>/process</code>
5. Ask your question with a request to <code>/query?text=</code>
6. Ready!

# Endpoints

<code>/process</code> -> the process to train your AI <br>
<code>/query?text=</code> -> this endpoint makes a question to your AI, send your question by the args

# About it

## Project description
the project is made with Flask, the project is a simple API that communicates with two services: OpenAI and ChromaDb.
ChromaDB serves as a vector database and thus create embeddings, which is expensive in terms of tokens or use refers to the OpenAI API, instead OpenAI is used in conjunction with the project in order to respond sensibly and conditionally with the indicated training

## Training
The training is based on using Markdown files with the content you want to train, it can be kitchen items or the desired theme. AI will understand and train

The AI will seek to classify the files by the main theme or h1 of the Markdowns which is "#", so your topic must be concise and clear so that the AI is easier to save and search for that topic

The AI will separate each topic or section (embedding) by a sub-sub-topic or a "###", from there, the AI will take the previous text as a separate section or topic and take the new one as a new section or topic. Eg :

'# Methods to center a div <br>
blablablabla' <br>
'###'
'# How to import this into JS' <br>
'blablabla. "'

# Sources to view

<strong>Flask</strong>: <https://flask.palletsprojects.com/en/3.0.x/>  <br>
<strong>ChromaDB</strong>: <https://docs.trychroma.com/> <br>
<strong>OpenAI</strong>: <https://platform.openai.com/> <br>
