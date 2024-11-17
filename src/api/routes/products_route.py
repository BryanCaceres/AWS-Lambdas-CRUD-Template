from flask import Blueprint, jsonify, request
from src.services.products_service import ProductsService

products_bp = Blueprint('products', __name__)

@products_bp.route('/<string:id>', methods=['GET'])
def get_product(id):
    products_service = ProductsService()
    product = products_service.get_product_by_pk(id)
    return jsonify(message=product)

@products_bp.route('/<string:id>', methods=['PATCH'])
def update_product(id):
    products_service = ProductsService()
    product = products_service.update_product(id, request.json)
    return jsonify(message=product), 201

@products_bp.route('/', methods=['POST'])
def create_product():
    products_service = ProductsService()
    product = products_service.create_product(request.json)
    return jsonify(message=product), 201

@products_bp.route('/', methods=['GET'])
def get_all_products():
    products_service = ProductsService()
    result = products_service.get_products()
    return jsonify(result)

@products_bp.route('/<string:id>', methods=['DELETE'])
def delete_product(id):
    products_service = ProductsService()
    result = products_service.delete_product(id)
    return jsonify(result)