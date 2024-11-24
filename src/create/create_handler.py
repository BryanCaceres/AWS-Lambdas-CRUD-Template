from typing import Dict, Any

from create_service import CreateService
from lambda_custom_layer import lambda_handler_decorator

service = CreateService()

@lambda_handler_decorator
def lambda_handler(event: Dict, context: Any) -> Dict:

    product_to_create = event['body']
    created_product = service.create(product_to_create)
    
    return {
        "statusCode": 201,
        "body": {"product": created_product},
        "message": "Product created successfully"
    }