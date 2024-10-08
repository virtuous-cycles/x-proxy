from flask import Flask
from api import api_bp
from config import Config
from services.x_service import XService
from services.oauth_setup import setup_and_validate_oauth
from services.airtable_service import AirtableService
from services.combined_services import CombinedServices
from error_handlers import register_error_handlers

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    oauth2_handler, oauth1_handler = setup_and_validate_oauth(app.config)

    oauth2_handler.start_refresh_thread()

    x_service = XService(oauth2_handler, oauth1_handler.api)
    app.x_service = x_service

    airtable_service = AirtableService(app.config)
    app.airtable_service = airtable_service

    combined_services = CombinedServices(airtable_service, x_service)
    app.combined_services = combined_services

    app.register_blueprint(api_bp, url_prefix='/api')

    # Register error handlers
    register_error_handlers(app)

    @app.route('/')
    def hello():
        return "Greetings, your pseudo-X-API is up and running!"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)