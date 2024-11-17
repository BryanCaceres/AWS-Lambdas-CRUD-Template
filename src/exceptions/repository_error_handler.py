from functools import wraps
from botocore.exceptions import ClientError
from src.exceptions.business_exceptions import BusinessException, DatabaseException, ResourceNotFoundException
import logging

def handle_repository_errors():
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except ClientError as e:
                error_code = e.response['Error']['Code']
                logging.error(f"DynamoDB Error: {error_code} - {str(e)}")
                
                error_mapping = {
                    'ConditionalCheckFailedException': BusinessException(
                        'El recurso no existe o fue modificado',
                        status_code=409
                    ),
                    'ProvisionedThroughputExceededException': DatabaseException(
                        'Capacidad de base de datos excedida',
                        status_code=429
                    )
                }
                
                raise error_mapping.get(error_code, DatabaseException(
                    'Error en operación de base de datos',
                    status_code=500
                )) from e
                
            except BusinessException as e:
                logging.error(f"Error de negocio en repositorio: {str(e)}")
                raise
                
            except Exception as e:
                logging.error(f"Error no manejado en repositorio: {str(e)}")
                raise DatabaseException(
                    'Error interno en operación de base de datos',
                    status_code=500
                ) from e
                
        return wrapped
    return decorator