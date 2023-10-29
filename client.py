import requests
from decouple import config

url = config("LOCAL_URL")+config("PORT")+'/train'

response = requests.post(url)
if response.status_code == 200:
    print('Client response:', response.text)
else:
    print('Error al hacer la solicitud:', response.status_code)