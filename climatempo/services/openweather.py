from core.api_service import ServicoApi

class ServicoOpenWeather(ServicoApi):
    def __init__(self, chave_api):
        self.url_base = "https://api.openweathermap.org/data/2.5"
        self.chave_api = chave_api

    def request_api(self, caminho, params):
        url = f"{self.url_base}/{caminho.lstrip('/')}"
        return self._request_json(url, params=params)

    def obter_clima(self, lat, lon, unidades="metric", idioma="pt_br"):
        params = {
            "lat": lat,
            "lon": lon,
            "units": unidades,
            "lang": idioma,
            "appid": self.chave_api,
        }

        return self.request_api("weather", params=params)
