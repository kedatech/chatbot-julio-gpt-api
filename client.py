import requests
from decouple import config

url = 'http://localhost:80/train'

response = requests.post(url)
if response.status_code == 200:
    print('Client response:', response.text)
else:
    print('Error al hacer la solicitud:', response.status_code)