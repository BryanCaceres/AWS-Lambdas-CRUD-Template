import functools
import json
import traceback
from typing import Dict, Any, Callable
from decimal import Decimal
from aws_lambda_powertools import Logger
from ..exeptions.exeptions import APIException

logger = Logger(service="LambdaUtils")

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler_decorator(lambda_handler: Callable) -> Callable:
    @functools.wraps(lambda_handler)
    def wrapper(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
        try:
            logger.info(f"Incoming Event: {event}")
            
            body = event.get('body', {})
            if isinstance(body, str):
                body_parsed = json.loads(body)
            else:
                body_parsed = body
            
            event['body'] = body_parsed
            logger.info(f"Body parsed: {body_parsed}")

            result = lambda_handler(event, context)
            
            response = {
                "statusCode": result.get("statusCode", 200),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({
                    "data": result.get("body", {}),
                    "error": False,
                    "status": {
                        "message": result.get("message", "Successful operation"),
                        "status_code": result.get("statusCode", 200)
                    }
                }, cls=DecimalEncoder)
            }
            
            logger.info(f"Response: {response}")
            return response

        except APIException as e:
            logger.warning(f"Custom API Exception: {str(e)}")
            error_response = {
                "statusCode": e.status_code,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({
                    "data": None,
                    "error": True,
                    "status": {
                        "message": e.message,
                        "status_code": e.status_code,
                        "error_code": e.__class__.__name__
                    }
                })
            }
            return error_response

        except Exception as e:
            logger.error(f"Internal Server Error: {str(e)}")
            logger.error(traceback.format_exc())
            
            error_response = {
                "statusCode": 500,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({
                    "data": None,
                    "error": True,
                    "status": {
                        "message": "Internal Server Error",
                        "status_code": 500
                    }
                })
            }
            return error_response
    
    return wrapper