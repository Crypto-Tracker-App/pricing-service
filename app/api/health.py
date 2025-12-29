from flask import Blueprint, jsonify
from sqlalchemy import text
from app import db
from app.utils.logger import get_logger

health_bp = Blueprint('health', __name__)
logger = get_logger(__name__)

@health_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint that verifies database connectivity."""
    try:
        # Attempt database connectivity check
        db.session.execute(text('SELECT 1'))
        return jsonify({
            'status': 'ok',
            'detail': 'database connection ok'
        }), 200
    except Exception as exc:
        logger.error("Health check failed", exc_info=True)
        return jsonify({ 
            'status': 'error',
            'detail': str(exc)
        }), 503
