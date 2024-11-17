import logging
import boto3
import uuid
from botocore.exceptions import ClientError
from src.config.settings import app_config
from typing import Dict, Optional, List, Tuple
from datetime import timezone, datetime
from src.exceptions.business_exceptions import ResourceNotFoundException

class ProductRepository:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name=app_config._config.aws_region)
        self.table = self.dynamodb.Table('products')

    def get_by_pk(self, uuid: str) -> Optional[Dict]:
        """
        Obtiene un producto por su UUID
        :param uuid: UUID del producto
        :return: Producto encontrado o None
        """
        try:
            response = self.table.get_item(
                Key={'uuid': uuid},
                ConsistentRead=True
            )
            
            product = response.get('Item')
            if not product:
                raise ResourceNotFoundException("Producto", uuid)
                
            logging.info(f'Producto obtenido: {product}')
            return product
        except ClientError as get_by_pk_error:
            logging.error(f'Error obteniendo producto de DynamoDB: {get_by_pk_error}')
            raise

    def get(self) -> List[Dict]:
        """
        Obtiene todos los productos de DynamoDB
        :return: Lista de productos en tabla products
        """
        try:
            response = self.table.scan()
            products = response.get('Items', [])
            logging.info(f'Productos obtenidos: {len(products)}')
            return products
        except ClientError as get_error:
            logging.error(f'Error obteniendo productos de DynamoDB: {get_error}')
            raise

    def create(self, product: Dict) -> Dict:
        """
        Crea un nuevo producto en DynamoDB usando UUID v4
        :param product: Diccionario con los datos del producto
        :return: Producto creado
        """
        try:
            product_uuid = str(uuid.uuid4())
            product['uuid'] = product_uuid
            current_time = datetime.now(timezone.utc).isoformat()
            product['created_at'] = current_time
            
            self.table.put_item(Item=product)
            logging.info(f'Producto creado: {product}')
            
            return product
        except ClientError as create_error:
            logging.error(f'Error creando producto en DynamoDB: {create_error}')
            raise
 
    def update(self, uuid: str, product_data: Dict) -> Dict:
        """
        Actualiza un producto existente
        :param uuid: UUID del producto
        :param product_data: Nuevos datos del producto
        :return: Producto actualizado
        """
        try:
            update_expression = "SET "
            expression_values = {}
            expression_names = {}
            
            # Actualizamos timestamp
            product_data['updated_at'] = datetime.now(timezone.utc).isoformat()
            
            for key, value in product_data.items():
                if key != 'uuid':  # No actualizamos el UUID
                    update_expression += f"#{key} = :{key}, "
                    expression_values[f":{key}"] = value
                    expression_names[f"#{key}"] = key

            update_expression = update_expression.rstrip(", ")
            
            response = self.table.update_item(
                Key={'uuid': uuid},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values,
                ExpressionAttributeNames=expression_names,
                ReturnValues="ALL_NEW"
            )
            
            updated_product = response.get('Attributes', {})
            logging.info(f'Producto actualizado: {updated_product}')
            
            return updated_product
        except ClientError as update_error:
            logging.error(f'Error actualizando producto en DynamoDB: {update_error}')
            raise

    def delete(self, uuid: str) -> Tuple[Dict, bool]:
        """
        Elimina un producto por su UUID y retorna sus datos
        :param uuid: UUID del producto
        :return: Tupla con (datos del producto, éxito de la eliminación)
        """
        try:
            product = self.get_by_pk(uuid)
            if not product:
                raise ResourceNotFoundException("Producto", uuid)
            
            self.table.delete_item(
                Key={'uuid': uuid},
                ConditionExpression='attribute_exists(#pk)',
                ExpressionAttributeNames={
                    '#pk': 'uuid'
                }
            )
            logging.info(f'Producto eliminado: {uuid}')
            return product, True
            
        except ClientError as delete_error:
            logging.error(f'Error al ejecutar delete_item: {delete_error}')
            if delete_error.response['Error']['Code'] == 'ConditionalCheckFailedException':
                return None, False
            raise delete_error