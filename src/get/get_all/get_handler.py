import boto3
from botocore.exceptions import ClientError
from typing import Dict, Optional, Any

from lambda_utils.decorators import lambda_handler_decorator

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('products')

@lambda_handler_decorator
def lambda_handler(event: Dict, context: Any) -> Dict:

    products = get_all()

    return {
        "statusCode": 200,
        "body": {"products": products}
    }

def get_all() -> Optional[Dict]:
    """
    Obtiene todos los productos de DynamoDB
    :return: Lista de productos en tabla products
    """
    try:
        response = table.scan()
        products = response.get('Items', [])
        
        if not products:
            raise ClientError("No se encontraron productos")
        
        return products
    
    except ClientError as e:
        raise e
    