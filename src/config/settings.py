from dataclasses import dataclass
from typing import Optional
from aws_lambda_powertools.utilities import parameters
import logging
import json
import os

@dataclass
class AppConfig:
    log_level: str
    aws_region: str = "us-east-1"

class ConfigurationManager:
    def __init__(self):
        self._config: Optional[AppConfig] = None
        self.load_configuration()

    def load_configuration(self) -> AppConfig:
        try:
            if os.getenv('AWS_SAM_LOCAL'):
                logging.info("Ejecucion local de la AWS Lambda")
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
                #Si es una ejecucion en AWS, se lee desde Parameter Store de AWS
                params = parameters.get_parameter(
                    "/flask-api/config",
                    transform="json",
                    force_fetch=True
                )

            self._config = AppConfig(
                log_level=params.get("LOG_LEVEL", "DEBUG"),
                aws_region=params.get("AWS_REGION", "us-east-1")
            )
            
            self._configure_logging()
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