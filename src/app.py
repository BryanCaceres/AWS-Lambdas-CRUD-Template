from flask import Flask
from src.api.routes.health_route import health_bp
from src.api.routes.products_route import products_bp

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(health_bp, url_prefix='/health')
    app.register_blueprint(products_bp, url_prefix='/products')

    return app