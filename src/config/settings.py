from dataclasses import dataclass
from typing import Optional
from aws_lambda_powertools.utilities import parameters
import logging

@dataclass
class AppConfig:
    log_level: str
    database_url: Optional[str] = None
    api_key: Optional[str] = None

class ConfigurationManager:
    def __init__(self):
        self._config: Optional[AppConfig] = None

    def load_configuration(self) -> AppConfig:
        try:
            params = parameters.get_parameter(
                f"/flask-api/config",
                transform="json",
                force_fetch=True
            )
            
            self._config = AppConfig(
                log_level=params.get("LOG_LEVEL", "DEBUG"),
                database_url=params.get("DATABASE_URL"),
                api_key=params.get("API_KEY")
            )
            
            self._configure_logging()
            return self._config
        except Exception as e:
            logging.error(f"Error loading configuration: {e}")
            raise

    def _configure_logging(self):
        logging.basicConfig(
            level=self._config.log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )