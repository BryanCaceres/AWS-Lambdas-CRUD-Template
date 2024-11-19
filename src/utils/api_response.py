from functools import wraps
from flask import jsonify
from typing import Any, Dict, Optional
import logging
from src.exceptions.business_exceptions import BusinessException, ResourceNotFoundException
from src.exceptions.error_handler import global_error_handler

class ApiResponse:
    @staticmethod
    def success(data: Optional[Any] = None, message: str = "Successful operation", status_code: int = 200, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Genera una respuesta de éxito estandarizada
        
        Args:
            data: data to return
            message: descriptive message
            status_code: HTTP status code
            metadata: optional additional information
        
        Returns:
            standard response dictionary
        """
        response = {
            "status": {
                "status_code": status_code,
                "message": message
            },
            "error": False,
            "data": data
        }
        
        if metadata:
            response["metadata"] = metadata
        
        return response

    @staticmethod
    def error(error: Exception, message: str = "Error in operation", status_code: int = 500) -> Dict[str, Any]:
        """
        Genera una respuesta de error estandarizada
        
        Args:
            message: error message
            status_code: HTTP status code
            details: additional error details
        
        Returns:
            standard error response dictionary
        """
        if isinstance(error, BusinessException):
            status_code = error.status_code
            message = error.message
        
        response = {
            "status": {
                "status_code": status_code,
                "message": message
            },
            "error": True,
            "details": {
                "exception_type": type(error).__name__,
                "exception_message": str(error)
            }
        }
        
        logging.error(f"API Error - {message}: {str(error)}")
        
        return response

def api_response(f):
    @wraps(f)
    @global_error_handler()
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        
        if isinstance(result, tuple):
            data, status_code = result
        else:
            data, status_code = result, 200
        response = {
            "error": False,
            "status": {
                "status_code": status_code,
                "message": "Successful operation"
            },
            "data": data
        }
        
        return jsonify(response), status_code
    
    return wrapper