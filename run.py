from flask import Flask
from app.routes.api_routes import api_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp, url_prefix="/")
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True,use_reloader=False)
