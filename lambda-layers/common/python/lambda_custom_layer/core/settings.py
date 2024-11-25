import boto3
import json

class Settings:
    def __init__(self):
        ssm = boto3.client('ssm', region_name='us-east-1')

        raw_parameters = ssm.get_parameter(
            Name='/lambda-crud-api/config/prod',
            WithDecryption=True
        )
        parameters = json.loads(raw_parameters['Parameter']['Value'])

        self.dynamodb_region_name = parameters.get('dynamodb_region_name', 'us-east-1')
        self.products_table = parameters.get('products_table', 'products')
        self.default_error_code = parameters.get('default_error_code', '500')
        self.default_error_message = parameters.get('default_error_message', 'Internal server error. Please try again later.')
        self.default_limit = parameters.get('default_limit', 50)
        self.log_level = parameters.get('log_level', 'ERROR')

settings = Settings()
