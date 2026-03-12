import time
import requests
import json


url = "http://apiadvisor.climatempo.com.br/api/v1/weather/locale/6071/current?token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"



while True:

    response = requests.get(url)

    if response.status_code == 200:
        
        data = response.json()

        print(data['data']['date'])

        with open('data.json', 'a') as json_file:
            json.dump(data, json_file)

    else:
        print(f"Erro: {response.status_code}")

    time.sleep(3600)
