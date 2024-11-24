from typing import Dict, Optional, Any
from update_service import UpdateService

service = UpdateService()

from lambda_custom_layer import lambda_handler_decorator

@lambda_handler_decorator
def lambda_handler(event: Dict, context: Any) -> Dict:

    product_update_data = event['body']   
    primary_key = event['pathParameters'].get('primary_key')

    updated_product = service.update(primary_key, product_update_data)
    
    return {
        "statusCode": 200,
        "body": {"updated_product": updated_product},
        "message": "Product updated successfully"
    }

    