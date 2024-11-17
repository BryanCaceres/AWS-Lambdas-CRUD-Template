from functools import wraps
from flask import jsonify
from src.exceptions.business_exceptions import BusinessException

def global_error_handler():
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                if isinstance(e, BusinessException):
                    return jsonify({
                        "error": True,
                        "status": {
                            "status_code": e.status_code,
                            "message": e.message
                        },
                        "details": {
                            "exception_type": type(e).__name__,
                            "exception_message": str(e)
                        }
                    }), e.status_code
                
                return jsonify({
                    "error": True,
                    "status": {
                        "status_code": 500,
                        "message": "Error interno del servidor"
                    },
                    "details": {
                        "exception_type": type(e).__name__,
                        "exception_message": str(e)
                    }
                }), 500
        return wrapped
    return decorator