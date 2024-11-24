import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any
import uuid
from datetime import datetime, timezone
from lambda_custom_layer import settings, APIException

class CreateService:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name=settings.dynamodb_region_name)
        self.table = self.dynamodb.Table(settings.products_table)

    def create(self, product: Dict) -> Dict:
        """
        Creates a new product in DynamoDB using UUID v4
        :param product: Dictionary with the product data
        :return: Created product
        """
        try:
            product_uuid = str(uuid.uuid4())
            product['uuid'] = product_uuid
            product['created_at'] = datetime.now(timezone.utc).isoformat()
                        
            self.table.put_item(Item=product)
            
            return product

        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'UnknownError')
            error_message = e.response.get('Error', {}).get('Message', 'An unexpected error occurred.')

            if error_code == 'UnknownError':
                error_code = settings.default_error_code
                error_message = settings.default_error_message

            raise APIException(f"Error creating product: {error_message}", status_code=int(error_code))