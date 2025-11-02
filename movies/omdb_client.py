from django.conf import settings
import requests

def find_data_omdb(titulo):
    try:
        api_key = getattr(settings, 'OMDB_API_KEY', None)
        url = "https://www.omdbapi.com/"
        params = {"t": titulo, "apikey": api_key}

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            dados = response.json()
            print(f" Dados recebidos  '{titulo}': {dados}")
            return dados
        else:
            print(f"falha na API OMDb para '{titulo}': {response.status_code}")
            return {}

    except Exception as e:
        print(f"erro na consulta OMDb para '{titulo}': {e}")
        return {}