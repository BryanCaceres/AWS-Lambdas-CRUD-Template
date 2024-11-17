from flask import Blueprint, request
from src.services.products_service import ProductsService
from src.utils.api_response import api_response, ApiResponse
from src.exceptions.business_exceptions import ResourceNotFoundException

products_bp = Blueprint('products', __name__)

products_service = ProductsService()

@products_bp.route('/', methods=['GET'])
@api_response
def get_all_products():
    try:
        query_result = products_service.get_products()
        return query_result, 200
    except Exception as e:
        response = ApiResponse.error(error=e, message=str(e), status_code=500)
        return response

@products_bp.route('/<string:pk>', methods=['GET'])
@api_response
def get_product(pk):
    try:
        product = products_service.get_product_by_pk(pk)
        return product, 200
    except ResourceNotFoundException as e:
        error_response = ApiResponse.error(e)
        return error_response, e.status_code
    except Exception as e:
        error_response = ApiResponse.error(e)
        return error_response

@products_bp.route('/', methods=['POST'])
@api_response
def create_product():
    try:
        created_product = products_service.create_product(request.json)
        return created_product, 201
    except ResourceNotFoundException as e:
        error_response = ApiResponse.error(e)
        return error_response, e.status_code
    except Exception as e:
        error_response = ApiResponse.error(e)
        return error_response

@products_bp.route('/<string:pk>', methods=['PATCH'])
@api_response
def update_product(pk):
    try:
        updated_product = products_service.update_product(pk, request.json)
        return updated_product, 200
    except ResourceNotFoundException as e:
        error_response = ApiResponse.error(e)
        return error_response, e.status_code
    except Exception as e:
        error_response = ApiResponse.error(e)
        return error_response

@products_bp.route('/<string:pk>', methods=['DELETE'])
@api_response
def delete_product(pk):
    try:
        deleted_product = products_service.delete_product(pk)
        return deleted_product, 200
    except ResourceNotFoundException as e:
        error_response = ApiResponse.error(e)
        return error_response, e.status_code
    except Exception as e:
        error_response = ApiResponse.error(e)
        return error_response