import base64
import requests

import os
os.environ['NO_PROXY'] = '127.0.0.1'

with open('input_image_demo.jpg', mode='rb') as file:
    img = file.read()   
encoded_image = base64.encodebytes(img).decode('utf-8')

resp = requests.post('127.0.0.1:5001/', data={'image':encoded_image})

print(resp)