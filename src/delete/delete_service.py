from typing import Dict, Any
import boto3
from botocore.exceptions import ClientError
from lambda_custom_layer import settings, ResourceNotFoundException, APIException

class DeleteService:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name=settings.dynamodb_region_name)
        self.table = self.dynamodb.Table(settings.products_table)

    def delete(self,primary_key: str) -> Dict:
        """
        Deletes a product by its UUID and returns its data
        :param primary_key: UUID of the product
        :return: Data of the deleted product
        """
        try:
            response = self.table.get_item(
                Key={'uuid': primary_key},
                ConsistentRead=True
            )

            product = response.get('Item')
            if not product:
                raise ResourceNotFoundException('product', primary_key)

            self.table.delete_item(
                Key={'uuid': primary_key},
                ConditionExpression='attribute_exists(#pk)',
                ExpressionAttributeNames={
                    '#pk': 'uuid'
                }
            )
            
            return product

        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'UnknownError')
            error_message = e.response.get('Error', {}).get('Message', 'An unexpected error occurred.')

            if error_code == 'UnknownError':
                error_code = settings.default_error_code
                error_message = settings.default_error_message

            raise APIException(f"Error deleting product: {error_message}", status_code=int(error_code))