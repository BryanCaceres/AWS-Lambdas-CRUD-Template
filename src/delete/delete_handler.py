import logging
import boto3
from botocore.exceptions import ClientError
from typing import Dict, Optional, Tuple
from aws_lambda_powertools import Logger
import json
import traceback
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
    try:
        logger.info(f'Event: {event}')
        primary_key = event['pathParameters'].get('primary_key')
        logger.info(f'Primary key: {primary_key}')
        deleted_product = delete(primary_key)
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "data": {
                    "deleted_product": deleted_product
                },
                "error": False,
                "status": {
                    "message": "Successful delete operation",
                    "status_code": 200
                }
            }, cls=DecimalEncoder)
        }
    except Exception as e:
        logger.info(f"Event: {event}")
        logger.error(f"Error en la operación de eliminación: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {
            "statusCode": 404 if "no encontrado" in str(e) else 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "data": None,
                "error": True,
                "status": {
                    "message": str(e),
                    "status_code": 404 if "no encontrado" in str(e) else 500
                }
            })
        }

def delete(primary_key: str) -> Dict:
    """
    Elimina un producto por su UUID y retorna sus datos
    :param primary_key: UUID del producto
    :return: Datos del producto eliminado
    """
    try:
        response = table.get_item(
            Key={'uuid': primary_key},
            ConsistentRead=True
        )

        product = response.get('Item')
        if not product:
            logger.error(f"Producto con UUID {primary_key} no encontrado")
            raise Exception(f"Producto con UUID {primary_key} no encontrado")

        table.delete_item(
            Key={'uuid': primary_key},
            ConditionExpression='attribute_exists(#pk)',
            ExpressionAttributeNames={
                '#pk': 'uuid'
            }
        )

        logger.info(f'Producto eliminado: {primary_key}')
        return product

    except ClientError as e:
        logger.error(f'Error al eliminar el producto: {e}')
        raise e