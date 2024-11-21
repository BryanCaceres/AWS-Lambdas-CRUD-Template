import logging
import boto3
from botocore.exceptions import ClientError
from typing import Dict
import uuid
from datetime import datetime, timezone

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('products')

def lambda_handler(event, context):

    product_to_create = event['body']
    created_product = create(product_to_create)
    
    return {
        "data": created_product,
        "error": False,
        "status": {
            "message": "Successful create operation",
            "status_code": 201
        }
    }

def create(product: Dict) -> Dict:
    """
    Crea un nuevo producto en DynamoDB usando UUID v4
    :param product: Diccionario con los datos del producto
    :return: Producto creado
    """
    try:
        product_uuid = str(uuid.uuid4())
        product['uuid'] = product_uuid
        product['created_at'] = datetime.now(timezone.utc).isoformat()
        
        table.put_item(Item=product)
        logging.info(f'Producto creado: {product}')
        
        return product
    except ClientError as e:
        logging.error(f'Error al crear el producto: {e}')
        raise e