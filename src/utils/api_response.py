from functools import wraps
from flask import jsonify
from typing import Any, Dict, Optional
import logging
from src.exceptions.business_exceptions import BusinessException, ResourceNotFoundException

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

def api_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            
            if isinstance(result, tuple):
                data, status_code = result
                if isinstance(data, dict) and data.get('error') is True:
                    return jsonify(data), status_code
                response = ApiResponse.success(data, status_code=status_code)
                return jsonify(response), status_code
            elif result is None:
                response = ApiResponse.success(None, status_code=204)
                return jsonify(response), 204
            else:
                response = ApiResponse.success(result)
                return jsonify(response)
        
        except ResourceNotFoundException as e:
            error_response = ApiResponse.error(e)
            return jsonify(error_response), e.status_code
        except Exception as e:
            error_response = ApiResponse.error(e)
            return jsonify(error_response), 500
    
    return wrapper