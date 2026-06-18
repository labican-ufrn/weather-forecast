from core.api_service import ServicoApi

class ServicoOpenMeteo(ServicoApi):
    def __init__(self):
        self.url = "https://api.open-meteo.com/v1/forecast"

    def request_api(self, params):
        return self._request_json(self.url, params=params)

    def obter_clima(self, lat, lon, timezone="America/Sao_Paulo"):
        variaveis_horas = [
            "temperature_2m",
            "relative_humidity_2m", 
            "dew_point_2m", 
            "rain", 
            "pressure_msl", 
            "surface_pressure", 
            "cloud_cover", 
            "visibility", 
            "wind_speed_10m", 
            "wind_direction_10m", 
            "soil_temperature_0cm", 
            "soil_temperature_6cm", 
            "soil_temperature_18cm", 
            "precipitation", 
            "precipitation_probability", 
            "evapotranspiration"
        ]

        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": ",".join(variaveis_horas),
            "timezone": timezone,
        }
        return self.request_api(params=params)