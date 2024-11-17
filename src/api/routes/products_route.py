from flask import Blueprint, jsonify, request
from src.services.products_service import ProductsService

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'])
def get_all_products():
    products_service = ProductsService()
    result = products_service.get_products()
    return jsonify(result)

@products_bp.route('/<string:pk>', methods=['GET'])
def get_product(pk):
    products_service = ProductsService()
    product = products_service.get_product_by_pk(pk)
    return jsonify(message=product)

@products_bp.route('/', methods=['POST'])
def create_product():
    products_service = ProductsService()
    product = products_service.create_product(request.json)
    return jsonify(message=product), 201

@products_bp.route('/<string:pk>', methods=['PATCH'])
def update_product(pk):
    products_service = ProductsService()
    product = products_service.update_product(pk, request.json)
    return jsonify(message=product), 201

@products_bp.route('/<string:pk>', methods=['DELETE'])
def delete_product(pk):
    products_service = ProductsService()
    result = products_service.delete_product(pk)
    return jsonify(result)
