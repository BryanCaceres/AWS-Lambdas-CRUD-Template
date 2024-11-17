from functools import wraps
from flask import jsonify
from typing import Any, Dict, Optional
import logging

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
    def error(error: Exception, message: str = "Error in operation", status_code: int = 500, error_code: Optional[str] = None) -> Dict[str, Any]:
        """
        Genera una respuesta de error estandarizada
        
        Args:
            message: error message
            status_code: HTTP status code
            details: additional error details
            error_code: specific error code
        
        Returns:
            standard error response dictionary
        """
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
        
        if error_code:
            response["error_code"] = error_code
        
        logging.error(f"API Error - {message}: {str(error)}")
        
        return response

def api_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            
            if isinstance(result, tuple):
                data, status_code = result
                response = ApiResponse.success(data, status_code=status_code)
                return jsonify(response)
            elif result is None:
                response = ApiResponse.success(None, status_code=204)
                return jsonify(response)
            else:
                response = ApiResponse.success(result)
                return jsonify(response)
        
        except Exception as e:
            error_details = {
                "exception_type": type(e).__name__,
                "exception_message": str(e)
            }
            response = ApiResponse.error(error=e, message="Internal server error", status_code=500, details=error_details)
            return jsonify(response), 500
    
    return wrapper