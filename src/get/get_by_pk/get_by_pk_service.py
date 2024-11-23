import boto3
from botocore.exceptions import ClientError
from typing import Dict, Optional, Any
from lambda_custom_layer import settings

class GetByPkService:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name=settings.region_name)
        self.table = self.dynamodb.Table(settings.products_table)

    def get_by_pk(self, primary_key: str) -> Optional[Dict]:
        """
        Obtiene un producto por su UUID
        :param primary_key: Primary key del producto a obtener
        :return: Producto encontrado o mensaje de error
        """
        try:
            response = self.table.get_item(
                Key={'uuid': primary_key},
                ConsistentRead=True
            )
            
            product = response.get('Item')
            if not product:
                raise ClientError("Producto no encontrado", primary_key)
            
            return product

        except ClientError as e:
            raise e