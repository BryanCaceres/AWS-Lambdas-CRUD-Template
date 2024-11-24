import boto3
from botocore.exceptions import ClientError
from typing import Dict, Optional, Any
from lambda_custom_layer import settings, APIException

class GetService:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name=settings.dynamodb_region_name)
        self.table = self.dynamodb.Table(settings.products_table)

    def get_all(self) -> Optional[Dict]:
        """
        Gets all products from DynamoDB
        :return: List of products in table products
        """
        try:
            response = self.table.scan()
            products = response.get('Items', [])            
            return products
        
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'UnknownError')
            error_message = e.response.get('Error', {}).get('Message', 'An unexpected error occurred.')

            if error_code == 'UnknownError':
                error_code = settings.default_error_code
                error_message = settings.default_error_message

            raise APIException(f"Error getting all products: {error_message}", status_code=int(error_code))