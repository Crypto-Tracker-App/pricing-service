from flask import Blueprint, jsonify, request
from app.services.coin_service import CoinService
from app.repositories.coin_repository import CoinRepository
from app.utils.logger import get_logger
from app.utils.json import to_jsonable

coin_bp = Blueprint('coin', __name__, url_prefix='/api')
logger = get_logger(__name__)

# Initialize service with a simple repository instance
_coin_service = CoinService(coin_repository=CoinRepository())


@coin_bp.route('/prices', methods=['GET'])
def get_prices():
    """
    Get current prices for specified coins.
    
    Query params:
        coins: Comma-separated list of coin IDs (e.g., bitcoin,ethereum)
        vs_currency: Currency to get price in (default: eur)
    
    Example:
        GET /api/prices?coins=bitcoin,ethereum&vs_currency=eur
    """
    try:
        # Get coin IDs from query params
        coins = request.args.get('coins', 'bitcoin')
        vs_currency = request.args.get('vs_currency', 'eur')
        
        coin_list = [c.strip() for c in coins.split(',')]
        
        logger.info(f"Fetching prices for coins: {coin_list}")
        response = _coin_service.get_prices(coin_list, vs_currency)
        logger.info(f"Successfully fetched prices for {len(coin_list)} coins")
        
        return jsonify({
            'status': 'success',
            'data': to_jsonable(response)
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to fetch prices: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@coin_bp.route('/fetch-prices', methods=['POST'])
def fetch_and_store_prices():
    """
    Fetch current prices and store them in the database.
    Intended to be called by CronJob.
    
    Body (optional):
        {
            "coins": ["bitcoin", "ethereum", "cardano"]
        }
    
    If no coins specified, fetches default list.
    """
    try:
        # Get coins from request body or use defaults
        data = request.get_json() if request.is_json else {}
        coin_list = data.get('coins', ['bitcoin', 'ethereum', 'cardano'])
        
        logger.info(f"Fetching and storing prices for {len(coin_list)} coins", extra={"coins": coin_list})
        response = _coin_service.fetch_and_store_prices(coin_list, vs_currency='usd')
        logger.info(f"Successfully fetched prices for storage", extra={"coin_count": len(response)})
        
        return jsonify({
            'status': 'success',
            'message': 'Fetched prices',
            'data': to_jsonable(response)
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to fetch and store prices: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@coin_bp.route('/history/<coin_id>', methods=['GET'])
def get_coin_history(coin_id):
    """
    Get historical price data for a specific coin.
    
    Path params:
        coin_id: CoinGecko coin ID (e.g., bitcoin)
    
    Query params:
        vs_currency: Currency (default: usd)
        days: Number of days (default: 7)
    
    Example:
        GET /api/history/bitcoin?vs_currency=usd&days=30
    """
    try:
        vs_currency = request.args.get('vs_currency', 'usd')
        days = request.args.get('days', '7')
        
        logger.info(f"Fetching {days} days of history for {coin_id}")
        response = _coin_service.get_coin_history(coin_id, vs_currency, days)
        logger.info(f"Successfully fetched history for {coin_id}")
        
        return jsonify({
            'status': 'success',
            'coin_id': coin_id,
            'data': to_jsonable(response)
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to fetch history for {coin_id}: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


