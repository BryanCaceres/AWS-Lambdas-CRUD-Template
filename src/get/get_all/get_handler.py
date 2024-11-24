from typing import Dict, Optional, Any
from lambda_custom_layer import lambda_handler_decorator
from get_service import GetService
import json

service = GetService()

@lambda_handler_decorator
def lambda_handler(event: Dict, context: Any) -> Dict:
    limit = int(event.get('queryStringParameters', {}).get('limit', 50))
    
    last_evaluated_key_str = event.get('queryStringParameters', {}).get('last_evaluated_key', None)
    last_evaluated_key = None
    if last_evaluated_key_str and last_evaluated_key_str.lower() not in ['null', 'none', '']:
        try:
            last_evaluated_key = json.loads(last_evaluated_key_str)
        except json.JSONDecodeError:
            last_evaluated_key = None

    products = service.get_all(last_evaluated_key, limit)

    return {
        "statusCode": 200,
        "body": {"products": products}
    }

    