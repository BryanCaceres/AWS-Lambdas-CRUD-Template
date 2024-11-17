import logging
import boto3
import uuid
from botocore.exceptions import ClientError
from src.config.settings import app_config
from typing import Dict, Optional, List
from datetime import timezone, datetime

class ProductRepository:
    def __init__(self):
        """
        Inicializa el repositorio con conexión a DynamoDB
        """
        self.dynamodb = boto3.resource('dynamodb', region_name=app_config.aws_region)
        self.table = self.dynamodb.Table('products')

    def create(self, product: Dict) -> Dict:
        """
        Crea un nuevo producto en DynamoDB usando UUID v4
        :param product: Diccionario con los datos del producto
        :return: Producto creado
        """
        try:
            product_id = str(uuid.uuid4())
            product['id'] = product_id
            current_time = datetime.now(timezone.utc).isoformat()
            product['created_at'] = current_time
            
            self.table.put_item(Item=product)
            logging.info(f'Producto creado: {product}')
            
            return product
        except ClientError as e:
            logging.error(f'Error creando producto en DynamoDB: {e}')
            raise

    def update(self, id: str, product_data: Dict) -> Dict:
        """
        Actualiza un producto existente
        :param id: ID del producto
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
                if key != 'id':  # No actualizamos el ID
                    update_expression += f"#{key} = :{key}, "
                    expression_values[f":{key}"] = value
                    expression_names[f"#{key}"] = key
            
            update_expression = update_expression.rstrip(", ")
            
            response = self.table.update_item(
                Key={'id': id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values,
                ExpressionAttributeNames=expression_names,
                ReturnValues="ALL_NEW"
            )
            
            updated_product = response.get('Attributes', {})
            logging.info(f'Producto actualizado: {updated_product}')
            
            return updated_product
        except ClientError as e:
            logging.error(f'Error actualizando producto en DynamoDB: {e}')
            raise

    def get_by_pk(self, id: str) -> Optional[Dict]:
        """
        Obtiene un producto por su ID
        :param id: ID del producto
        :return: Producto encontrado o None
        """
        try:
            response = self.table.get_item(
                Key={'id': id},
                ConsistentRead=True
            )
            
            product = response.get('Item')
            if not product:
                logging.error(f'No existe el producto con id {id}')
                return None
                
            logging.info(f'Producto obtenido: {product}')
            return product
        except ClientError as e:
            logging.error(f'Error obteniendo producto de DynamoDB: {e}')
            raise

    def get(self) -> List[Dict]:
        """
        Obtiene todos los productos de DynamoDB
        :return: Lista de productos
        """
        try:
            response = self.table.scan()
            products = response.get('Items', [])
            logging.info(f'Productos obtenidos: {len(products)}')
            return products
        except ClientError as e:
            logging.error(f'Error obteniendo productos de DynamoDB: {e}')
            raise

    def delete(self, id: str) -> bool:
        """
        Elimina un producto por su ID
        :param id: ID del producto
        :return: True si se eliminó correctamente
        """
        try:
            self.table.delete_item(
                Key={'id': id},
                ConditionExpression='attribute_exists(id)'
            )
            logging.info(f'Producto eliminado: {id}')
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                logging.error(f'No existe el producto con id {id}')
                return False
            logging.error(f'Error eliminando producto en DynamoDB: {e}')
            raise