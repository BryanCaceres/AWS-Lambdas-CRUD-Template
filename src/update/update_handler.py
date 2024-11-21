import logging
import boto3
import json
from botocore.exceptions import ClientError
from typing import Dict, Optional
from decimal import Decimal
from datetime import datetime, timezone
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
    try:
        logger.info(f'Event: {event}')
        
        # Parseamos el body si viene como string
        product_to_update = event['body']
        if isinstance(product_to_update, str):
            product_to_update = json.loads(product_to_update)
            
        primary_key = event['pathParameters'].get('primary_key')
        logger.info(f'Primary key: {primary_key}')
        logger.info(f'Product to update: {product_to_update}')
        
        updated_product = update(primary_key, product_to_update)
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "data": {"updated_product": updated_product},
                "error": False,
                "status": {
                    "message": "Successful update operation",
                    "status_code": 200
                }
            }, cls=DecimalEncoder)
        }
    except Exception as e:
        logger.error(f'Error en la operación de actualización: {e}')
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "data": None,
                "error": True,
                "status": {
                    "message": str(e),
                    "status_code": 500
                }
            }, cls=DecimalEncoder)
        }

def update(primary_key: str, product_data: Dict) -> Optional[Dict]:
    """
    Actualiza un producto existente
    :param primary_key: Primary key del producto
    :param product_data: Nuevos datos del producto
    :return: Producto actualizado
    """
    try:
        update_expression = "SET "
        expression_values = {}
        expression_names = {}
        
        product_data['updated_at'] = datetime.now(timezone.utc).isoformat()
        
        for key, value in product_data.items():
            if key != 'uuid':  # No actualizamos el UUID
                update_expression += f"#{key} = :{key}, "
                expression_values[f":{key}"] = value
                expression_names[f"#{key}"] = key

        update_expression = update_expression.rstrip(", ")
        
        response = table.update_item(
            Key={'uuid': primary_key},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values,
            ExpressionAttributeNames=expression_names,
            ReturnValues="ALL_NEW"
        )
        
        updated_product = response.get('Attributes', {})
        logger.info(f'Producto actualizado: {updated_product}')
        
        return updated_product
    
    except ClientError as e:
        logger.error(f'Error al obtener los productos: {e}')
        raise e
    