import logging
import boto3
from botocore.exceptions import ClientError
from typing import Dict, Optional
from aws_lambda_powertools import Logger
import json
from decimal import Decimal

logger = Logger(service="ProductsAPI")

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('products')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    logger.info(f'Event: {event}')
    
    primary_key = event['pathParameters'].get('primary_key')
    logger.info(f'Primary key: {primary_key}')
    
    try:
        product = get_by_pk(primary_key)
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "data": product,
                "error": False,
                "status": {
                    "message": "Successful operation",
                    "status_code": 200
                }
            }, cls=DecimalEncoder)
        }
    except ClientError as e:
        logger.error(f'Error al obtener el producto: {e}')
        return {
            "statusCode": 404,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "data": None,
                "error": True,
                "status": {
                    "message": str(e),
                    "status_code": 404
                }
            })
        }

def get_by_pk(primary_key: str) -> Optional[Dict]:
    """
    Obtiene un producto por su UUID
    :param primary_key: Primary key del producto a obtener
    :return: Producto encontrado o mensaje de error
    """
    try:
        response = table.get_item(
            Key={'uuid': primary_key},
            ConsistentRead=True
        )
        
        product = response.get('Item')
        if not product:
            raise ClientError("Producto no encontrado", primary_key)
        
        logger.info(f'Producto obtenido: {product}')
        return product

    except ClientError as e:
        logger.error(f'Error al obtener el producto: {e}')
        raise e