import boto3
from botocore.exceptions import ClientError
from typing import Dict, Optional, Any
from datetime import datetime, timezone

from lambda_utils.decorators import lambda_handler_decorator

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('products')

@lambda_handler_decorator
def lambda_handler(event: Dict, context: Any) -> Dict:

    product_to_update = event['body']   
    primary_key = event['pathParameters'].get('primary_key')

    updated_product = update(primary_key, product_to_update)
    
    return {
        "statusCode": 200,
        "body": {"updated_product": updated_product},
        "message": "Producto actualizado exitosamente"
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
        
        return updated_product
    
    except ClientError as e:
        raise e
    