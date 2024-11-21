import logging
import boto3
from botocore.exceptions import ClientError
from typing import Dict, Optional, Tuple

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('products')

def lambda_handler(event, context):

    primary_key = event['pathParameters'].get('primary_key')
    deleted_product = delete(primary_key)
    
    return {
        "data": {
            "deleted_product": deleted_product
        },
        "error": False,
        "status": {
            "message": "Successful delete operation",
            "status_code": 200
        }
    }

def delete(primary_key: str) -> Tuple[Dict, bool]:
    """
    Elimina un producto por su UUID y retorna sus datos
    :param uuid: UUID del producto
    :return: Tupla con (datos del producto, éxito de la eliminación)
    """
    try:
        response = table.get_item(
            Key={'uuid': primary_key},
        ConsistentRead=True
        )

        product = response.get('Item')
        if not product:
            raise ClientError("Producto", primary_key)

        table.delete_item(
            Key={'uuid': primary_key},
            ConditionExpression='attribute_exists(#pk)',
            ExpressionAttributeNames={
                '#pk': 'uuid'
            }
        )

        logging.info(f'Producto eliminado: {primary_key}')

        return product

    except ClientError as e:
        logging.error(f'Error al eliminar el producto: {e}')
        raise e