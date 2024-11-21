import logging
import boto3
import json
from botocore.exceptions import ClientError
from typing import Dict
import uuid
from datetime import datetime, timezone
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
import json

logger = Logger(service="ProductsAPI")

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('products')

def lambda_handler(event: dict, context: LambdaContext):
    logger.append_keys(request_id=context.aws_request_id)
    
    try:
        logger.info("Iniciando creación de producto")
        
        if 'body' not in event:
            logger.warning("Request sin body")
            raise ValueError("El body es requerido")
        
        body = event['body']
        if isinstance(body, str):
            product_to_create = json.loads(body)
            logger.debug("Body parseado correctamente", extra={"body": product_to_create})
        else:
            product_to_create = body
        
        created_product = create(product_to_create)
        logger.info("Producto creado exitosamente", extra={"product": created_product})
        
        return {
            "statusCode": 201,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "data": created_product,
                "error": False,
                "status": {
                    "message": "Successful create operation",
                    "status_code": 201
                }
            })
        }
    except Exception as e:
        logger.exception("Error en el proceso de creación")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "data": None,
                "error": True,
                "status": {
                    "message": str(e),
                    "status_code": 500
                }
            })
        }

def create(product: Dict) -> Dict:
    """
    Crea un nuevo producto en DynamoDB usando UUID v4
    :param product: Diccionario con los datos del producto
    :return: Producto creado
    """
    try:
        product_uuid = str(uuid.uuid4())
        product['uuid'] = product_uuid
        product['created_at'] = datetime.now(timezone.utc).isoformat()
        
        table.put_item(Item=product)
        logger.info(f'Producto creado: {product}')
        
        return product
    except ClientError as e:
        logger.error(f'Error al crear el producto: {e}')
        raise e