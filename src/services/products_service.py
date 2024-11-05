import logging
from src.repositories.client_repositorie import ClientRepository
from typing import Dict

class ProductsService:
    def __init__(self):
        self.client_repository = ClientRepository()

    def create_product(self, product: Dict) -> Dict:
        """
        :param product: Diccionario con los datos del producto según el esquema de validación del endpoint
        :return: Instancia del producto creado
        """
        try:
            logging.info(f'Se quiere crear un producto llamado {product["name"]} con el precio {product["price"]}')
            
            product_created = self.client_repository.create_product(product)
            
            return product_created

        except Exception as e:
            logging.error(f'Error al crear el producto: {e}')
            return {'error': 'Error al crear el producto'}, 500

    def update_product(self, id: int, product_data: Dict) -> Dict:
        """
        :param id: Identificador del producto a actualizar
        :param product_data: Diccionario con los datos del producto según el esquema de validación del endpoint
        :return: Instancia del producto ya actualizado
        """
        pass
    
    def get_product_by_id(self, id: int) -> Dict:
        try: 
            logging.info(f'Acaban de solicitar el producto con id {id}')
            
            found_product = self.client_repository.get_product_by_id(id)
            
            return found_product
        except Exception as e:
            logging.error(f'Error al obtener el producto: {e}')
            return {'error': 'Error al obtener el producto'}, 500