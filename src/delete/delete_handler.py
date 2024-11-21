from typing import Dict, Any
import boto3
from botocore.exceptions import ClientError

from lambda_utils.decorators import lambda_handler_decorator

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('products')

@lambda_handler_decorator
def lambda_handler(event: Dict, context: Any) -> Dict:

    primary_key = event['pathParameters'].get('primary_key')
    deleted_product = delete(primary_key)
    
    return {
        "statusCode": 200,
        "body": {"deleted_product": deleted_product},
        "message": "Producto eliminado exitosamente"
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
            raise Exception(f"Producto con UUID {primary_key} no encontrado")

        table.delete_item(
            Key={'uuid': primary_key},
            ConditionExpression='attribute_exists(#pk)',
            ExpressionAttributeNames={
                '#pk': 'uuid'
            }
        )

        return product

    except ClientError as e:
        raise e