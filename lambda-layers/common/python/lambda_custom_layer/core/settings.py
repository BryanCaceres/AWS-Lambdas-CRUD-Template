import boto3
import json
import functools

@functools.lru_cache(maxsize=1)
def get_ssm_parameters():
    ssm = boto3.client('ssm', region_name='us-east-1')
    raw_parameters = ssm.get_parameter(
        Name='/lambda-crud-api/config/prod',
        WithDecryption=True
    )
    return json.loads(raw_parameters['Parameter']['Value'])

class Settings:
    _instance = None
    _parameters = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._parameters = get_ssm_parameters()
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.dynamodb_region_name = self._parameters.get('dynamodb_region_name', 'us-east-1')
            self.products_table = self._parameters.get('products_table', 'products')
            self.default_error_code = self._parameters.get('default_error_code', '500')
            self.default_error_message = self._parameters.get('default_error_message', 'Internal server error. Please try again later.')
            self.default_limit = self._parameters.get('default_limit', 50)
            self.log_level = self._parameters.get('log_level', 'ERROR')
            self.initialized = True

settings = Settings()
