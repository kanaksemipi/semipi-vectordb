from flask import Flask
from app.routes.api_routes import api_bp
from app.chroma_client import init_chroma_collection

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp)
    
    # Initialize ChromaDB collection on app start
    init_chroma_collection()
    
    return app
