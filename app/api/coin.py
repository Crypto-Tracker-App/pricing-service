from flask import Blueprint, jsonify, request
from app.services.coin_service import CoinService
from app.repositories.coin_repository import CoinRepository
from app.utils.logger import get_logger

coin_bp = Blueprint('coin', __name__, url_prefix='/api')
logger = get_logger(__name__)

# Initialize service with a simple repository instance
_coin_service = CoinService(coin_repository=CoinRepository())


@coin_bp.route('/top-coins', methods=['GET'])
def get_top_coins():
    """
    Get top coins by market cap rank.
    
    Query params:
        limit: Number of coins to return (default: 10, max: 100)
        offset: Number of coins to skip for pagination (default: 0)
    
    Example:
        GET /api/top-coins?limit=20&offset=0
    """
    try:
        # Get pagination params
        limit = min(int(request.args.get('limit', 10)), 100)  # Cap at 100
        offset = int(request.args.get('offset', 0))
        
        logger.info(f"Fetching top {limit} coins (offset: {offset})")
        top_coins = _coin_service.get_top_coins(top_n=limit, skip_n=offset)
        logger.info(f"Successfully fetched {len(top_coins)} coins")
        
        return jsonify({
            'status': 'success',
            'data': top_coins,
            'pagination': {
                'limit': limit,
                'offset': offset,
                'returned': len(top_coins)
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to fetch top coins: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@coin_bp.route('/coin/<coin_id>', methods=['GET'])
def get_coin(coin_id: str):
    """
    Get a single coin (metadata + market data) by its ID.
    
    Path params:
        coin_id: CoinGecko coin id (e.g., bitcoin, ethereum)
    
    Example:
        GET /api/coin/bitcoin
    """
    try:
        coin_data = _coin_service.get_coin_by_id(coin_id)
        return jsonify({
            'status': 'success',
            'data': coin_data
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to fetch coin data: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
    
