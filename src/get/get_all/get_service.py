import boto3
from botocore.exceptions import ClientError
from typing import Dict, Optional, Any
from lambda_custom_layer import settings

class GetService:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name=settings.region_name)
        self.table = self.dynamodb.Table(settings.products_table)

    def get_all(self) -> Optional[Dict]:
        """
        Obtiene todos los productos de DynamoDB
        :return: Lista de productos en tabla products
        """
        try:
            response = self.table.scan()
            products = response.get('Items', [])
            
            if not products:
                raise ClientError("No se encontraron productos")
            
            return products
        
        except ClientError as e:
            raise e