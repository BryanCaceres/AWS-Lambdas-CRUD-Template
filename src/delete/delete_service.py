from typing import Dict, Any
import boto3
from botocore.exceptions import ClientError
from lambda_custom_layer import settings

class DeleteService:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name=settings.region_name)
        self.table = self.dynamodb.Table(settings.products_table)

    def delete(self,primary_key: str) -> Dict:
        """
        Elimina un producto por su UUID y retorna sus datos
        :param primary_key: UUID del producto
        :return: Datos del producto eliminado
        """
        try:
            response = self.table.get_item(
                Key={'uuid': primary_key},
                ConsistentRead=True
            )

            product = response.get('Item')
            if not product:
                raise Exception(f"Producto con UUID {primary_key} no encontrado")

            self.table.delete_item(
                Key={'uuid': primary_key},
                ConditionExpression='attribute_exists(#pk)',
                ExpressionAttributeNames={
                    '#pk': 'uuid'
                }
            )
            
            return product

        except ClientError as e:
            raise e