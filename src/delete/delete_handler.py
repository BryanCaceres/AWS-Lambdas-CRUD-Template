from typing import Dict, Any

from delete_service import DeleteService
from lambda_custom_layer import lambda_handler_decorator

service = DeleteService()

@lambda_handler_decorator
def lambda_handler(event: Dict, context: Any) -> Dict:

    primary_key = event['pathParameters'].get('primary_key')
    deleted_product = service.delete(primary_key)
    
    return {
        "statusCode": 200,
        "body": {"deleted_product": deleted_product},
        "message": "Producto eliminado exitosamente"
    }
