from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__)

@health_bp.route('/')
def health_check():
    return jsonify(message='Que hace un bellezon como tú, en una api como esta?')