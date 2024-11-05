from enum import Enum
import os
import logging

class EnvironmentType(Enum):
    DEV = "DEV"
    PROD = "PROD"

class BaseConfig:
    def __init__(self):
        self.AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
        self.configure_logging()

    def configure_logging(self):
        raise NotImplementedError("Este método debe ser implementado en las subclases")

class DevConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.STAGE = EnvironmentType.DEV
        self.LOG_LEVEL = "DEBUG"
        self.configure_logging()

    def configure_logging(self):
        logging.basicConfig(level=self.LOG_LEVEL)
        logging.info("Logging configurado en modo DEV: nivel DEBUG")

class ProdConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.STAGE = EnvironmentType.PROD
        self.LOG_LEVEL = "ERROR"
        self.configure_logging()

    def configure_logging(self):
        logging.basicConfig(level=self.LOG_LEVEL)
        logging.info("Logging configurado en modo PROD: nivel ERROR")

def get_config() -> BaseConfig:
    stage = os.getenv("STAGE", "DEV")
    if stage == "PROD":
        return ProdConfig()
    return DevConfig()

app_config = get_config()