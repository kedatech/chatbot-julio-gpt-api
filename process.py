import chromadb
from chromadb.config import Settings
from gradio_client import Client
import glob

document_id = 1
chroma_client = chromadb.PersistentClient(path="/local_collections",settings=Settings(allow_reset=True))

def find_markdowns():
    folder_path = 'Markdowns/'
    files = [(f, open(f, 'rb')) for f in glob.glob(folder_path + '*.md')]
    return files
    

def process_files(documents):
    collection = chroma_client.create_collection(name="julio_collections")
    
    for file in documents:
        print("processing file: " + file["filename"])
        markdown_text = file["content"]
        chunks = split_text(markdown_text)
        document_title = get_title(markdown_text)
        generate_embeddings(chunks, document_title, file["filename"], collection)
        print(chunks," ",document_title, " ",file["filename"])
    
def generate_embeddings(chunks, document_title, file_name, collection):
    global document_id
    for chunk in chunks:
        collection.add(
            metadatas={
                "document_title": document_title if document_title is not None else "",
                "file_name": file_name
            },
            documents=chunk,
            ids=[str(document_id)]
        )
        
        document_id += 1

def get_title(file):
    lines = file.split("\n")
    if lines[0].startswith("# "):
        title = lines[0][2:]
        return title
    else:
        return ""

def split_text(file):
    separator = "\n### "
    return file.split(separator)

def speechTotext():
    client = Client("https://sandiago21-automatic-speech-recognition-spanish.hf.space/")
    result = client.predict(
        "audios/sample.ogg",	
        api_name="/predict")
    print("Speeched: ", result)
    return result

def query_collection(query):
    collection = chroma_client.get_collection(name="julio_collections")
    return collection.query(
        query_texts=[query],
        n_results=2,
    )
