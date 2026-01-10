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
    """Get top coins by market cap rank
    ---
    tags:
      - Coins
    summary: Retrieve top cryptocurrency coins
    description: Returns a list of top cryptocurrencies sorted by market cap rank, with pagination support
    parameters:
      - name: limit
        in: query
        type: integer
        required: false
        default: 10
        minimum: 1
        maximum: 100
        description: Number of coins to return (max 100)
      - name: offset
        in: query
        type: integer
        required: false
        default: 0
        minimum: 0
        description: Number of coins to skip for pagination
    responses:
      200:
        description: Successfully retrieved top coins
        schema:
          type: object
          properties:
            status:
              type: string
              example: success
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                    example: bitcoin
                  symbol:
                    type: string
                    example: btc
                  name:
                    type: string
                    example: Bitcoin
                  current_price:
                    type: number
                    example: 43250.50
                  market_cap:
                    type: number
                    example: 847832100000
                  market_cap_rank:
                    type: integer
                    example: 1
            pagination:
              type: object
              properties:
                limit:
                  type: integer
                  example: 10
                offset:
                  type: integer
                  example: 0
                returned:
                  type: integer
                  example: 10
      500:
        description: Internal server error
        schema:
          type: object
          properties:
            status:
              type: string
              example: error
            message:
              type: string
              example: Database connection failed
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


@coin_bp.route('/coin-ids', methods=['GET'])
def get_coin_ids():
    """Get IDs of top coins by market cap rank
    ---
    tags:
      - Coins
    summary: Retrieve coin IDs
    description: Returns a list of IDs for top cryptocurrencies sorted by market cap rank, with pagination support
    parameters:
      - name: limit
        in: query
        type: integer
        required: false
        default: 10
        minimum: 1
        maximum: 100
        description: Number of coin IDs to return (max 100)
      - name: offset
        in: query
        type: integer
        required: false
        default: 0
        minimum: 0
        description: Number of coins to skip for pagination
    responses:
      200:
        description: Successfully retrieved coin IDs
        schema:
          type: object
          properties:
            status:
              type: string
              example: success
            data:
              type: array
              items:
                type: string
              example: ["bitcoin", "ethereum", "binancecoin"]
            pagination:
              type: object
              properties:
                limit:
                  type: integer
                  example: 10
                offset:
                  type: integer
                  example: 0
                returned:
                  type: integer
                  example: 3
      500:
        description: Internal server error
        schema:
          type: object
          properties:
            status:
              type: string
              example: error
            message:
              type: string
              example: Database connection failed
    """
    try:
        # Get pagination params
        limit = min(int(request.args.get('limit', 10)), 100)  # Cap at 100
        offset = int(request.args.get('offset', 0))
        
        logger.info(f"Fetching IDs of top {limit} coins (offset: {offset})")
        top_coins = _coin_service.get_top_coins(top_n=limit, skip_n=offset)
        
        # Extract only the IDs
        coin_ids = [coin['id'] for coin in top_coins]
        logger.info(f"Successfully fetched {len(coin_ids)} coin IDs")
        
        return jsonify({
            'status': 'success',
            'data': coin_ids,
            'pagination': {
                'limit': limit,
                'offset': offset,
                'returned': len(coin_ids)
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to fetch coin IDs: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@coin_bp.route('/coin/<coin_id>', methods=['GET'])
def get_coin(coin_id: str):
    """Get detailed information for a specific coin
    ---
    tags:
      - Coins
    summary: Retrieve coin details by ID
    description: Returns metadata and market data for a specific cryptocurrency
    parameters:
      - name: coin_id
        in: path
        type: string
        required: true
        description: CoinGecko coin identifier (e.g., bitcoin, ethereum)
        example: bitcoin
    responses:
      200:
        description: Successfully retrieved coin data
        schema:
          type: object
          properties:
            status:
              type: string
              example: success
            data:
              type: object
              properties:
                id:
                  type: string
                  example: bitcoin
                symbol:
                  type: string
                  example: btc
                name:
                  type: string
                  example: Bitcoin
                current_price:
                  type: number
                  example: 43250.50
                market_cap:
                  type: number
                  example: 847832100000
                market_cap_rank:
                  type: integer
                  example: 1
                total_volume:
                  type: number
                  example: 25678000000
      500:
        description: Internal server error
        schema:
          type: object
          properties:
            status:
              type: string
              example: error
            message:
              type: string
              example: Coin not found
    """
    try:
        coin_data = _coin_service.get_coin_by_id(coin_id)
        
        if coin_data is None:
            logger.warning(f"Coin not found: {coin_id}")
            return jsonify({
                'status': 'error',
                'message': f'Coin with ID "{coin_id}" not found'
            }), 404
        
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
