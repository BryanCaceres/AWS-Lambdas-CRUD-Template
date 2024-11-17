from flask import Blueprint
from src.utils.api_response import ApiResponse
from src.config.settings import app_config

health_bp = Blueprint('health', __name__)

@health_bp.route('/')
def health_check():
    return ApiResponse.success(
        data={
            "config": app_config._config.__dict__
        },
        message='Que hace un bellezon como tú, en una api como esta?'
    )
