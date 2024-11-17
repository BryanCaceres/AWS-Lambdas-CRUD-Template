import logging
from src.repositories.product_repository import ProductRepository
from typing import Dict
from src.exceptions.business_exceptions import ResourceNotFoundException

class ProductsService:
    def __init__(self):
        self.product_repository = ProductRepository()

    def get_product_by_pk(self, id: int) -> Dict:
        try: 
            logging.info(f'Acaban de solicitar el producto con id {id}')
            
            found_product = self.product_repository.get_by_pk(id)
            
            return found_product

        except ResourceNotFoundException as e:
            logging.error(f'Producto no encontrado: {e}')
            raise e
        except Exception as e:
            logging.error(f'Error al obtener el producto: {e}')
            return {'error': 'Error al obtener el producto'}, 500

    def get_products(self) -> Dict:
        """
        Obtiene todos los productos
        :return: Lista de productos o mensaje de error
        """
        try:
            logging.info('Solicitando todos los productos')
            products = self.product_repository.get()
            return {'products': products}

        except Exception as e:
            logging.error(f'Error al obtener productos: {e}')
            return {'error': 'Error al obtener los productos'}, 500

    def create_product(self, product: Dict) -> Dict:
        """
        :param product: Diccionario con los datos del producto según el esquema de validación del endpoint
        :return: Instancia del producto creado
        """
        try:
            logging.info(f'Se quiere crear un producto llamado {product["name"]} con el precio {product["price"]}')
            
            product_created = self.product_repository.create(product)
            
            return { "created_product": product_created }

        except Exception as e:
            logging.error(f'Error al crear el producto: {e}')
            return {'error': 'Error al crear el producto'}, 500

    def update_product(self, id: int, product_data: Dict) -> Dict:
        """
        :param id: Identificador del producto a actualizar
        :param product_data: Diccionario con los datos del producto según el esquema de validación del endpoint
        :return: Instancia del producto ya actualizado
        """
        try:
            logging.info(f'Se quiere actualizar el producto con id {id}')
            # Primero verificamos que exista
            self.product_repository.get_by_pk(id)
            updated_product = self.product_repository.update(id, product_data)
            return { "product_new_values": updated_product }

        except ResourceNotFoundException as e:
            logging.error(f'Producto no encontrado para actualizar: {e}')
            raise e
        except Exception as e:
            logging.error(f'Error al actualizar el producto: {e}')
            return {'error': 'Error al actualizar el producto'}, 500

    def delete_product(self, id: str) -> Dict:
        """
        Elimina un producto por su ID
        :param id: ID del producto a eliminar
        :return: Datos del producto eliminado o mensaje de error
        """
        try:
            logging.info(f'Eliminando producto con id {id}')
            deleted_product, was_deleted = self.product_repository.delete(id)
            
            if not deleted_product:
                return {'error': 'Producto no encontrado'}, 404
            
            return { "deleted_product": deleted_product }

        except ResourceNotFoundException as e:
            logging.error(f'Producto no encontrado para actualizar: {e}')
            raise e
        except Exception as e:
            logging.error(f'Error al eliminar el producto: {e}')
            return {'error': 'Error al eliminar el producto'}, 500
