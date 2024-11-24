from typing import Dict, Any
from get_by_pk_service import GetByPkService
from lambda_custom_layer import lambda_handler_decorator

service = GetByPkService()

@lambda_handler_decorator
def lambda_handler(event: Dict, context: Any) -> Dict:
    
    primary_key = event['pathParameters'].get('primary_key')
    product = service.get_by_pk(primary_key)

    return {
        "statusCode": 200,
        "body": {"product": product}
    }
