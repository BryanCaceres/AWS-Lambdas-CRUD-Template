from dataclasses import dataclass
from typing import Optional
from aws_lambda_powertools.utilities import parameters
import logging
import json
import os
import json
import os

@dataclass
class AppConfig:
    log_level: str
    aws_region: str = "us-east-1"
    aws_region: str = "us-east-1"

class ConfigurationManager:
    def __init__(self):
        self._config: Optional[AppConfig] = None
        self.load_configuration()
        self.load_configuration()

    def load_configuration(self) -> AppConfig:
        try:
            if os.getenv('AWS_SAM_LOCAL'):
                logging.info("Ejecución local de la AWS Lambda")
                try:
                    with open('env.json', 'r') as f:
                        params = json.load(f)
                except FileNotFoundError:
                    logging.warning("env.json no encontrado. Usando valores por defecto")
                    params = {
                        "LOG_LEVEL": "DEBUG",
                        "AWS_REGION": "us-east-1"
                    }
            else:
                logging.info("Obteniendo configuración desde Parameter Store")
                try:
                    params = parameters.get_parameter(
                        "/flask-api/config",
                        transform="json",
                        decrypt=True,
                        force_fetch=True
                    )
                    logging.debug(f"Parámetros obtenidos: {params}")
                except Exception as e:
                    logging.error(f"Error al obtener parámetros: {str(e)}")
                    logging.error(f"Tipo de error: {type(e).__name__}")
                    raise

            self._config = AppConfig(
                log_level=params.get("LOG_LEVEL", "DEBUG"),
                aws_region=params.get("AWS_REGION", "us-east-1")
                aws_region=params.get("AWS_REGION", "us-east-1")
            )
            
            self._configure_logging()
            logging.debug(f"Configuración cargada: {self._config}")
            logging.debug(f"Configuración cargada: {self._config}")
            return self._config
        except Exception as e:
            logging.error(f"Error loading configuration: {e}")
            raise

    def _configure_logging(self):
        logging.basicConfig(
            level=self._config.log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

app_config = ConfigurationManager()
app_config = ConfigurationManager()