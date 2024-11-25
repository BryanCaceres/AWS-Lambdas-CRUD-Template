from typing import Dict, Optional, Any
from lambda_custom_layer import lambda_handler_decorator, settings
from get_service import GetService
import json

service = GetService()

@lambda_handler_decorator
def lambda_handler(event: Dict, context: Any) -> Dict:
    query_params = event.get('queryStringParameters') or {}
    
    limit = int(query_params.get('limit', settings.default_limit))
    
    last_evaluated_key_str = query_params.get('last_evaluated_key')
    last_evaluated_key = None
    if last_evaluated_key_str and last_evaluated_key_str.lower() not in ['null', 'none', '']:
        try:
            last_evaluated_key = json.loads(last_evaluated_key_str)
        except json.JSONDecodeError:
            last_evaluated_key = {}

    products = service.get_all(last_evaluated_key, limit)

    return {
        "statusCode": 200,
        "body": {"products": products}
    }

    