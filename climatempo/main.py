import os
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv
from collector import coletar_e_salvar

load_dotenv()

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

def _bool_env(nome, padrao=False):
    valor = os.environ.get(nome)
    if valor is None:
        return padrao
    return valor.strip().lower() in ("1", "true", "sim", "yes")


def rodar_uma_vez():
    logger.info("Modo uma_vez iniciado")
    coletar_e_salvar()
    logger.info("Modo uma_vez finalizado")


def rodar_agendador():
    executar_imediato = _bool_env("COLETA_IMEDIATA_ON_START", padrao=True)
    timezone_agendador = os.environ.get("TZ", "UTC")

    logger.info(
        "Agendador iniciado | timezone=%s | coleta_imediata=%s",
        timezone_agendador,
        executar_imediato,
    )

    if executar_imediato:
        logger.info("Executando coleta imediata na inicializacao")
        coletar_e_salvar()

    scheduler = BlockingScheduler(timezone=timezone_agendador)

    scheduler.add_job(
        coletar_e_salvar,
        trigger="cron",
        hour="*",
        minute=0,
        second=0,
        id="coleta_horaria",
        replace_existing=True,
        coalesce=True,
        max_instances=1,
    )

    logger.info("Job coleta_horaria agendado para toda hora cheia")
    scheduler.start()


if __name__ == "__main__":
    modo = os.environ.get("MODO_EXECUCAO", "agendador")
    logger.info("Inicializacao do processo | modo=%s", modo)
    if modo == "uma_vez":
        rodar_uma_vez()
    else:
        rodar_agendador()
