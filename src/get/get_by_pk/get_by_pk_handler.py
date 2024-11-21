import logging
import boto3
from botocore.exceptions import ClientError
from typing import Dict, Optional

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('products')

def lambda_handler(event, context):

    primary_key = event['pathParameters'].get('primary_key')
    product = get_by_pk(primary_key)
    
    return {
        "data": product,
        "error": False,
        "status": {
            "message": "Successful operation",
            "status_code": 200
        }
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
            raise ClientError("Producto", primary_key)
        
        logging.info(f'Producto obtenido: {product}')
        return product

    except ClientError as e:
        logging.error(f'Error al obtener el producto: {e}')
        raise e