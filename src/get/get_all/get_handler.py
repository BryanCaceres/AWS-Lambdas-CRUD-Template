import logging
import boto3
from botocore.exceptions import ClientError
from typing import Dict, Optional

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('products')

def lambda_handler(event, context):

    products = get_all()
    
    return {
        "data": products,
        "error": False,
        "status": {
            "message": "Successful operation",
            "status_code": 200
        }
    }

def get_all() -> Optional[Dict]:
    """
    Obtiene todos los productos de DynamoDB
    :return: Lista de productos en tabla products
    """
    try:
        response = table.scan()
        products = response.get('Items', [])
        logging.info(f'Productos obtenidos: {len(products)}')
        
        if not products:
            raise ClientError("No se encontraron productos")
        
        return products
    
    except ClientError as e:
        logging.error(f'Error al obtener los productos: {e}')
        raise e
    