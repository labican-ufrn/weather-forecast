from core.api_service import ServicoApi

class ServicoWeatherApi(ServicoApi):
    def __init__(self, chave_api):
        self.url_base = "https://api.weatherapi.com/v1"
        self.chave_api = chave_api

    def request_api(self, caminho, params):
        url = f"{self.url_base}/{caminho.lstrip('/')}"
        return self._request_json(url, params=params)

    def obter_clima(self, consulta_cidade, idioma="pt"):
        params = {
            "key": self.chave_api,
            "q": consulta_cidade,
            "lang": idioma,
        }
        dados = self.request_api("current.json", params=params)
        return dados.get("current", {})
