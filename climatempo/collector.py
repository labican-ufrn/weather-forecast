import os
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

#from services.weatherapi import ServicoWeatherApi
#from services.openweather import ServicoOpenWeather
from services.openmeteo import ServicoOpenMeteo
#from services.hgbrasil import ServicoHGBrasil
from db.firebase import BancoFirebase

logger = logging.getLogger(__name__)


def _env_obrigatoria(nome):
    valor = os.environ.get(nome)
    if not valor:
        raise ValueError(f"Variavel de ambiente {nome} nao definida")
    return valor



def _timestamp_coleta(horario_execucao=None):
    tz_brasilia = ZoneInfo("America/Sao_Paulo")

    if horario_execucao is None:
        base = datetime.now(tz_brasilia)
    elif horario_execucao.tzinfo is None:
        base = horario_execucao.replace(tzinfo=tz_brasilia)
    else:
        base = horario_execucao.astimezone(tz_brasilia)

    return base.isoformat(timespec="seconds")


def _config_cidade():
    return {
        "consulta_cidade": os.environ.get("CIDADE_CONSULTA", "Caico,RN,BR"),
        "lat": float(os.environ.get("CIDADE_LAT", "-6.4583")),
        "lon": float(os.environ.get("CIDADE_LON", "-37.0978")),
        "timezone": os.environ.get("CIDADE_TIMEZONE", "America/Sao_Paulo"),
    }


def buscar_todos():
    #weatherapi = ServicoWeatherApi(chave_api=_env_obrigatoria("CHAVE_WEATHERAPI"))
    #openweather = ServicoOpenWeather(chave_api=_env_obrigatoria("CHAVE_OPENWEATHER"))
    openmeteo = ServicoOpenMeteo()
    #hgbrasil = ServicoHGBrasil()

    config_cidade = _config_cidade()

    coletas = {
        "openmeteo": (
            openmeteo.obter_clima,
            {
                "lat": config_cidade["lat"],
                "lon": config_cidade["lon"],
                "timezone": config_cidade["timezone"],
            },
        ),
    }

    payload = {}
    erros = {}

    for nome_servico, (funcao, parametros) in coletas.items():
        logger.info("Iniciando requisicao do servico %s", nome_servico)
        try:
            payload[nome_servico] = funcao(**parametros)
            logger.info("Servico %s retornou dados com sucesso", nome_servico)

        except Exception:
            erros[nome_servico] = "falha_na_requisicao"
            logger.exception(
                "Servico %s falhou; continuando com os demais",
                nome_servico
            )


    return payload


def salvar_no_firebase(payload, horario_execucao=None):
    firebase = BancoFirebase()

    timestamp = _timestamp_coleta(horario_execucao)
    dados = {
        "timestamp": timestamp,
        "payload": payload,
    }

    firebase.inserir("weather", dados)


def coletar_e_salvar(horario_execucao=None):
    logger.info("Iniciando coleta meteorologica")
    try:
        payload = buscar_todos()
        #servicos_com_sucesso = [
           # nome for nome in ("weatherapi", "openweather", "openmeteo", "hgbrasil")
           # if nome in payload
       # ]

        #if not servicos_com_sucesso:
            #raise RuntimeError("Nenhum servico retornou dados para salvar")

        salvar_no_firebase(payload, horario_execucao=horario_execucao)
        #logger.info(
            #"Coleta salva com sucesso no Firebase com %s servicos",
            #len(servicos_com_sucesso),
        #)
        return payload
    except Exception:
        logger.exception("Falha na coleta meteorologica")
        raise
