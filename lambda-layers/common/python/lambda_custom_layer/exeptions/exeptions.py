class APIException(Exception):
    """Base exception for all API errors"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class ResourceNotFoundException(APIException):
    """Exception for resources not found"""
    def __init__(self, resource: str, identifier: str):
        message = f"{resource} with identifier {identifier} not found"
        super().__init__(message, status_code=404)

class ValidationException(APIException):
    """Exception for validation errors"""
    def __init__(self, message: str):
        super().__init__(message, status_code=400)

class ConflictException(APIException):
    """Exception for resource conflicts"""
    def __init__(self, message: str):
        super().__init__(message, status_code=409)