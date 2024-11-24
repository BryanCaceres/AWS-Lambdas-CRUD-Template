import boto3
from botocore.exceptions import ClientError
from typing import Dict, Optional, Any
from datetime import datetime, timezone
from lambda_custom_layer import settings, ResourceNotFoundException, APIException

class UpdateService:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name=settings.dynamodb_region_name)
        self.table = self.dynamodb.Table(settings.products_table)

    def update(self, primary_key: str, product_data: Dict) -> Optional[Dict]:
        """
        Updates an existing product
        :param primary_key: Primary key of the product
        :param product_data: New data of the product
        :return: Updated product
        """
        try:
            response = self.table.get_item(
                Key={'uuid': primary_key},
                ConsistentRead=True
            )

            product = response.get('Item')
            if not product:
                raise ResourceNotFoundException('product', primary_key)

            update_expression = "SET "
            expression_values = {}
            expression_names = {}
            
            product_data['updated_at'] = datetime.now(timezone.utc).isoformat()
            
            for key, value in product_data.items():
                if key != 'uuid':  # No actualizamos el UUID
                    update_expression += f"#{key} = :{key}, "
                    expression_values[f":{key}"] = value
                    expression_names[f"#{key}"] = key

            update_expression = update_expression.rstrip(", ")
            
            response = self.table.update_item(
                Key={'uuid': primary_key},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values,
                ExpressionAttributeNames=expression_names,
                ReturnValues="ALL_NEW"
            )
            
            updated_product = response.get('Attributes', {})

            return updated_product
        
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'UnknownError')
            error_message = e.response.get('Error', {}).get('Message', 'An unexpected error occurred.')

            if error_code == 'UnknownError':
                error_code = settings.default_error_code
                error_message = settings.default_error_message

            raise APIException(f"Error editing product: {error_message}", status_code=int(error_code))