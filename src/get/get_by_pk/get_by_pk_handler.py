import boto3
from botocore.exceptions import ClientError
from typing import Dict, Optional, Any

from lambda_utils.decorators import lambda_handler_decorator

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('products')


@lambda_handler_decorator
def lambda_handler(event: Dict, context: Any) -> Dict:
    
    primary_key = event['pathParameters'].get('primary_key')
    product = get_by_pk(primary_key)

    return {
        "statusCode": 200,
        "body": {"product": product}
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
        
        return product

    except ClientError as e:
        raise e