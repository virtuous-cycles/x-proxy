from flask import jsonify
from services.rate_limit_handler import RateLimitExceeded

def register_error_handlers(app):
    @app.errorhandler(RateLimitExceeded)
    def handle_rate_limit_error(error):
        app.logger.warning(f"Rate limit exceeded: {error}")
        return jsonify({
            'error': 'Rate limit exceeded',
            'message': str(error),
            'retry_after': error.retry_after
        }), 429

    @app.errorhandler(Exception)
    def handle_generic_error(error):
        app.logger.error(f"An unexpected error occurred: {error}", exc_info=True)
        return jsonify({
            'error': 'An unexpected error occurred',
            'message': str(error)
        }), 500