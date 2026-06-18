import os
from core.api_service import ServicoApi

class ServicoHGBrasil(ServicoApi):
    def __init__(self):
        self.url = "https://api.hgbrasil.com/weather"
        self.chave_api = os.environ.get("CHAVE_HGBRASIL")
        if not self.chave_api:
            raise ValueError("Variavel de ambiente CHAVE_HGBRASIL nao definida")

    def request_api(self, params):
        return self._request_json(self.url, params=params)

    def obter_clima(self, lat=None, lon=None):
        params = {
            "lat": lat or float(os.environ.get("CIDADE_LAT", "-6.4583")),
            "lon": lon or float(os.environ.get("CIDADE_LON", "-37.0978")),
            "key": self.chave_api,
        }
        return self.request_api(params=params)
