import boto3
from botocore.exceptions import ClientError
from typing import Dict, Optional, Any
from datetime import datetime, timezone
from lambda_custom_layer import settings

class UpdateService:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name=settings.region_name)
        self.table = self.dynamodb.Table(settings.products_table)

    def update(self,primary_key: str, product_data: Dict) -> Optional[Dict]:
        """
        Actualiza un producto existente
        :param primary_key: Primary key del producto
        :param product_data: Nuevos datos del producto
        :return: Producto actualizado
        """
        try:
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
            raise e