import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any
import uuid
from datetime import datetime, timezone
from lambda_custom_layer import settings

class CreateService:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name=settings.region_name)
        self.table = self.dynamodb.Table(settings.products_table)

    def create(self, product: Dict) -> Dict:
        """
        Crea un nuevo producto en DynamoDB usando UUID v4
        :param product: Diccionario con los datos del producto
        :return: Producto creado
        """
        try:
            product_uuid = str(uuid.uuid4())
            product['uuid'] = product_uuid
            product['created_at'] = datetime.now(timezone.utc).isoformat()
            
            self.table.put_item(Item=product)
            
            return product

        except ClientError as e:
            raise e