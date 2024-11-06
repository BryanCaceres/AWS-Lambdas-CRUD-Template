import logging

class ProductRepository:
    def create(self, product):
        """
        :param product: Instancia del producto a crear
        :return: Instancia del producto creado
        """
        #TODO: Implementar la lógica para crear un producto en tu base de datos
        
        product_created = product
        product_created['id'] = 1313
        
        logging.info(f'Producto creado: {product_created}')

        return product_created

    def update(self, id, product_data):
        """
        :param id: Identificador del producto a actualizar
        :param product_data: Diccionario con los nuevos datos del producto a actualizar
        :return: Instancia del producto actualizado
        """
        dummy_product = {
            'id': id,
            'name': product_data['name'],
            'price': product_data['price']
        }
        
        logging.info(f'Producto actualizado: {dummy_product}')
        
        return dummy_product
    
    def get_by_id(self, id):
        """
        :param id: Identificador del producto a obtener
        :return: Instancia del producto obtenido
        """
        products_fake_list = {
            666: {
                'id': 1,
                'name': 'Embergadura_product',
                'price': 666
            }
        }
        try:
            dummy_product = products_fake_list[id]
            logging.info(f'Producto obtenido: {dummy_product}')

            return dummy_product
        except Exception as e:
            logging.error(f'No existe el producto con id {id}')
            return {'error': 'No existe el producto con id'}, 404