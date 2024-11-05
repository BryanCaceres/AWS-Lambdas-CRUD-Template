from flask import Blueprint, jsonify, request
from src.services.products_service import ProductsService

products_bp = Blueprint('products', __name__)
# La validación de los datos de entrada ya está hecha por API Gateway

@products_bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    products_service = ProductsService()
    product = products_service.get_product_by_id(id)
    return jsonify(message=product)

@products_bp.route('/<int:id>', methods=['PUT'])
def update_product(id):
    products_service = ProductsService()
    product = products_service.update_product(id, request.json)
    return jsonify(message=product), 201

@products_bp.route('/', methods=['POST'])
def create_product():
    products_service = ProductsService()
    product = products_service.create_product(request.json)
    return jsonify(message=product), 201