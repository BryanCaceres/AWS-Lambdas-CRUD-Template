import logging
import boto3
from botocore.exceptions import ClientError
from typing import Dict, Optional
import json
from decimal import Decimal
from aws_lambda_powertools import Logger

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
    products = get_all()
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "data": products,
            "error": False,
            "status": {
                "message": "Successful operation",
                "status_code": 200
            }
        }, cls=DecimalEncoder)
    }

def get_all() -> Optional[Dict]:
    """
    Obtiene todos los productos de DynamoDB
    :return: Lista de productos en tabla products
    """
    try:
        response = table.scan()
        products = response.get('Items', [])
        logger.info(f'Productos obtenidos: {len(products)}')
        
        if not products:
            raise ClientError("No se encontraron productos")
        
        return products
    
    except ClientError as e:
        logger.error(f'Error al obtener los productos: {e}')
        raise e
    