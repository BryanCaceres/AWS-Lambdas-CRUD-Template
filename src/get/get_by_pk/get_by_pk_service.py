import boto3
from botocore.exceptions import ClientError
from typing import Dict, Optional, Any
from lambda_custom_layer import settings, ResourceNotFoundException, APIException

class GetByPkService:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name=settings.dynamodb_region_name)
        self.table = self.dynamodb.Table(settings.products_table)

    def get_by_pk(self, primary_key: str) -> Optional[Dict]:
        """
        Gets a product by its UUID
        :param primary_key: Primary key of the product to get
        :return: Found product or error message
        """
        try:
            response = self.table.get_item(
                Key={'uuid': primary_key},
                ConsistentRead=True
            )
            
            product = response.get('Item')
            if not product:
                raise ResourceNotFoundException('product', primary_key)

            return product

        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'UnknownError')
            error_message = e.response.get('Error', {}).get('Message', 'An unexpected error occurred.')

            if error_code == 'UnknownError':
                error_code = settings.default_error_code
                error_message = settings.default_error_message

            raise APIException(f"Error getting product by UUID: {error_message}", status_code=int(error_code))