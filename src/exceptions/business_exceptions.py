from typing import Optional

class BusinessException(Exception):
    """Excepción base para errores de negocio"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class ResourceNotFoundException(BusinessException):
    """Excepción para recursos no encontrados"""
    def __init__(self, resource: str, resource_pk: Optional[str] = None):
        message = f"{resource} no encontrado"
        if resource_pk:
            message = f"{resource} con id {resource_pk} no encontrado"
        super().__init__(message=message, status_code=404)