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
            product_uuid = str(uuid.uuid4())
            product['uuid'] = product_uuid
            current_time = datetime.now(timezone.utc).isoformat()
            product['created_at'] = current_time
            
            self.table.put_item(Item=product)
            logging.info(f'Producto creado: {product}')
            
            return product
        except ClientError as e:
            logging.error(f'Error creando producto en DynamoDB: {e}')
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
        except ClientError as e:
            logging.error(f'Error actualizando producto en DynamoDB: {e}')
            raise

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
                logging.error(f'No existe el producto con uuid {uuid}')
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

    def delete(self, uuid: str) -> bool:
        """
        Elimina un producto por su UUID
        :param uuid: UUID del producto
        :return: True si se eliminó correctamente
        """
        try:
            self.table.delete_item(
                Key={'uuid': uuid},
                ConditionExpression='attribute_exists(uuid)'
            )
            logging.info(f'Producto eliminado: {uuid}')
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                logging.error(f'No existe el producto con uuid {uuid}')
                return False
            logging.error(f'Error eliminando producto en DynamoDB: {e}')
            raise