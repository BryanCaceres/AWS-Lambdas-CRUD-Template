from typing import Dict, Optional, Any
from lambda_custom_layer import lambda_handler_decorator
from get_service import GetService

service = GetService()

@lambda_handler_decorator
def lambda_handler(event: Dict, context: Any) -> Dict:

    products = service.get_all()

    return {
        "statusCode": 200,
        "body": {"products": products}
    }

    