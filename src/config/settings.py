from dataclasses import dataclass
from typing import Optional
from aws_lambda_powertools.utilities import parameters
import logging
import json
import os

@dataclass
class AppConfig:
    log_level: str
    database_url: Optional[str] = None
    api_key: Optional[str] = None
    jwt_secret_key: Optional[str] = None
    aws_region: str = "us-east-1"

class ConfigurationManager:
    def __init__(self):
        self._config: Optional[AppConfig] = None

    def load_configuration(self) -> AppConfig:
        try:
            if os.getenv('AWS_SAM_LOCAL'):
                #Si es una ejecucion local, se lee el archivo env.json
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
                #Si es una ejecucion en AWS, se lee desde Parameter Store
                params = parameters.get_parameter(
                    "/flask-api/config",
                    transform="json",
                    force_fetch=True
                )
            
            self._config = AppConfig(
                log_level=params.get("LOG_LEVEL", "DEBUG"),
                database_url=params.get("DATABASE_URL"),
                api_key=params.get("API_KEY"),
                jwt_secret_key=params.get("JWT_SECRET_KEY"),
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

app_config = ConfigurationManager().load_configuration()