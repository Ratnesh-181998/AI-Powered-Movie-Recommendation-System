from flask import Flask
from flask_cors import CORS
from app.api.routes import api_bp
from app.services.data_service import data_service
from app.utils.logger import log_startup, log_shutdown, api_logger, log_error
import traceback

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    CORS(app)  # Enable CORS for React frontend
    
    # Register Blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Initialize data on startup (optional here, can be done in run.py)
    # But doing it here ensures it's ready if imported elsewhere
    # However, for faster startup in tests, maybe skip?
    # We'll let run.py handle the explicit load call for better logging control
    
    return app
