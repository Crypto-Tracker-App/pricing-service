import jwt
import logging
import os
from flask import request, jsonify, g, current_app
from functools import wraps

logger = logging.getLogger(__name__)

ALGORITHM = "HS256"

def get_secret_key():
    """Get SECRET_KEY from Flask app config, with fallback to environment variable."""
    try:
        secret = current_app.config.get('SECRET_KEY')
        if secret:
            logger.debug(f"Got SECRET_KEY from Flask config: {secret[:20]}...")
            return secret
    except RuntimeError:
        # Outside of app context
        logger.debug("Not in app context, falling back to environment variable")
    
    secret = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    logger.debug(f"Using SECRET_KEY from environment: {secret[:20]}...")
    return secret

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            logger.warning("No Authorization header provided")
            return jsonify({'error': 'Unauthorized', 'message': 'Missing Authorization header'}), 401
        
        try:
            # Extract token from "Bearer <token>" format
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                logger.warning(f"Invalid Authorization header format: {auth_header[:20]}...")
                return jsonify({'error': 'Unauthorized', 'message': 'Invalid Authorization header format'}), 401
            
            token = parts[1]
            logger.debug(f"Attempting to decode token: {token[:30]}...")
            
            # Get SECRET_KEY from current_app config
            secret_key = get_secret_key()
            logger.debug(f"Using SECRET_KEY (first 20 chars): {secret_key[:20]}...")
            
            try:
                payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
                logger.debug(f"Token decoded successfully. Payload: {payload}")
            except jwt.DecodeError as e:
                logger.error(f"JWT Decode error: {str(e)}")
                return jsonify({'error': 'Unauthorized', 'message': 'Invalid token format'}), 401
            
            user_id = payload.get('user_id')
            username = payload.get('username')
            
            if not user_id:
                logger.warning("Token missing user_id")
                return jsonify({'error': 'Unauthorized', 'message': 'Invalid token payload'}), 401
            
            logger.info(f"User authenticated: user_id={user_id}, username={username}")
            g.current_user = {
                'user_id': user_id,
                'username': username
            }
            # Also set on request for backwards compatibility
            request.user_id = user_id
            request.username = username
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            logger.error("Token has expired")
            return jsonify({'error': 'Unauthorized', 'message': 'Token expired'}), 401
        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid token: {str(e)}")
            return jsonify({'error': 'Unauthorized', 'message': 'Invalid token'}), 401
        except Exception as e:
            logger.error(f"Authorization error: {str(e)}", exc_info=True)
            return jsonify({'error': 'Unauthorized', 'message': 'Authorization failed'}), 401
    return decorated

def require_auth(f):
    """Alias for auth_required for backwards compatibility"""
    return auth_required(f)
