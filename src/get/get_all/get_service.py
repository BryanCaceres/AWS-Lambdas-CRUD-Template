import boto3
from botocore.exceptions import ClientError
from typing import Dict, Optional, Any
from lambda_custom_layer import settings, APIException

class GetService:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name=settings.dynamodb_region_name)
        self.table = self.dynamodb.Table(settings.products_table)

    def get_all(self, last_evaluated_key: Optional[Dict] = None, limit: int = 50) -> Dict:
        """
        Gets all products from DynamoDB
        :params:
            last_evaluated_key: Last evaluated key from previous scan
            limit: Limit of products to return
        :return: List of products in table products
        """
        try:
            params = {
                'Limit': limit,
                'ReturnConsumedCapacity': 'TOTAL'
            }
            
            if last_evaluated_key:
                params['ExclusiveStartKey'] = last_evaluated_key
            
            response = self.table.scan(**params)
            
            return {
                'items': response.get('Items', []),
                'last_evaluated_key': response.get('LastEvaluatedKey'),
                'consumed_capacity': response.get('ConsumedCapacity')
            }

        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'UnknownError')
            error_message = e.response.get('Error', {}).get('Message', 'An unexpected error occurred.')

            if error_code == 'UnknownError':
                error_code = settings.default_error_code
                error_message = settings.default_error_message

            raise APIException(f"Error getting all products: {error_message}", status_code=int(error_code))
        
