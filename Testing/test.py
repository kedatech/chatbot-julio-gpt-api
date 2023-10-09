import requests
import os, json
import glob
from env import BACKEND_SERVER


url = BACKEND_SERVER + '/process'

def process_backend():
    folder_path = 'Markdowns/'
    files = [(f, open(f, 'rb')) for f in glob.glob(folder_path + '*.md')]
    
    return files

    
# if not files:
#     print('No se encontraron  en la carpeta Markdowns/')
# else:
#     response = requests.post(url)
#     if response.status_code == 200:
#         print('Respuesta del servidor:', response.text)
#     else:
#         print('Error al hacer la solicitud:', response.status_code)
    

