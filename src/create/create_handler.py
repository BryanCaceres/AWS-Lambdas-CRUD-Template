import logging
import boto3
import json
from botocore.exceptions import ClientError
from typing import Dict
import uuid
from datetime import datetime, timezone
import json

from lambda_utils.decorators import lambda_handler_decorator

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('products')

@lambda_handler_decorator
def lambda_handler(event, context):

    product_to_create = event['body']
    created_product = create(product_to_create)
    
    return {
        "statusCode": 201,
        "body": {"product": created_product}
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
        
        return product
    except ClientError as e:
        raise e