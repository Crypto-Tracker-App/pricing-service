from datetime import datetime, timezone
from sqlalchemy import insert
from app.utils.coingecko import client
from app.repositories.coin_repository import CoinRepository
from app.models.coinModels import supported_coins

class CoinService:
    def __init__(self, coin_repository: CoinRepository, vs_currency: str = "eur"):
        self.coin_repository = coin_repository
        self.vs_currency = vs_currency

    def get_top_coins(self, top_n: int = 10, skip_n: int = 0):
        """
        Fetch top N coins by market cap rank from the database.
        
        Args:
            top_n: Number of coins to return (default: 10)
            skip_n: Number of coins to skip for pagination (default: 0)
            
        Returns:
            list[dict]: List of coin data with market information, ordered by market_cap_rank
        """
        # Query MarketData ordered by market_cap_rank, with pagination
        market_data_records = (
            self.coin_repository.session.query(self.coin_repository.MarketData)
            .join(self.coin_repository.Coin)
            .filter(self.coin_repository.MarketData.market_cap_rank.isnot(None))
            .order_by(self.coin_repository.MarketData.market_cap_rank.asc())
            .offset(skip_n)
            .limit(top_n)
            .all()
        )
        
        # Build response with coin and market data
        top_coins = []
        for market_data in market_data_records:
            coin_info = {
                'id': market_data.coin.id,
                'symbol': market_data.coin.symbol,
                'name': market_data.coin.name,
                'image': market_data.coin.image,
                'current_price': market_data.current_price
            }
            top_coins.append(coin_info)
        
        return top_coins

    def get_coin_by_id(self, coin_id: str):
        """
        Fetch a coin by its ID along with its market data.
        
        Args:
            coin_id: The unique identifier of the coin.
            
        Returns:
            dict: Coin data with market information, or None if not found.
        """
        
        market_data = (
            self.coin_repository.session.query(self.coin_repository.MarketData)
            .join(self.coin_repository.Coin)
            .filter(self.coin_repository.Coin.id == coin_id)
            .first()
        )

        if not market_data:
            return None
        
        coin_info = {
            'id': market_data.coin.id,
            'symbol': market_data.coin.symbol,
            'name': market_data.coin.name,
            'image': market_data.coin.image,
            'current_price': market_data.current_price,
            'market_cap': market_data.market_cap,
            'market_cap_rank': market_data.market_cap_rank,
            'total_volume': market_data.total_volume,
            'high_24h': market_data.high_24h,
            'low_24h': market_data.low_24h,
            'price_change_24h': market_data.price_change_24h,
            'price_change_percentage_24h': market_data.price_change_percentage_24h,
            'circulating_supply': market_data.circulating_supply,
            'total_supply': market_data.total_supply,
            'max_supply': market_data.max_supply,
            'sparkline_in_7d': market_data.sparkline_in_7d,
            'last_updated': market_data.last_updated.isoformat() if market_data.last_updated else None,
            'created_at': market_data.created_at.isoformat() if market_data.created_at else None,
        }
        
        return coin_info

    def seed_database(self):
        """
        Seed the database with supported coins and their initial market data.
        
        Fetches all supported coins from CoinGecko markets API and stores:
        - Coin metadata (id, symbol, name, image)
        - Initial market data (price, market cap, volume, 24h changes, supply info)
        
        Idempotent: Only seeds if database is empty. Safe to call multiple times.
        
        Raises:
            Exception: If API call or database insertion fails.
        """
        # Check if database has any coins
        existing_coins = self.coin_repository.session.query(self.coin_repository.Coin).count()
        if existing_coins != 0:
            return  # Database already seeded

        # Fetch current market data
        market_data_dicts = self.getCurrentMaketDataForUpdate()

        # Prepare bulk insert lists
        coins_to_add = []
        market_data_to_add = []
        
        for coin_dict in market_data_dicts:            
            # Create coin
            coin = self.coin_repository.Coin(
                id=coin_dict.get('id'),
                symbol=coin_dict.get('symbol'),
                name=coin_dict.get('name'),
                image=coin_dict.get('image')
            )
            coins_to_add.append(coin)
            
            # Create market data for this coin
            market_data = self.coin_repository.MarketData(
                coin_id=coin_dict.get('id'),
                current_price=coin_dict.get('current_price'),
                market_cap=coin_dict.get('market_cap'),
                market_cap_rank=coin_dict.get('market_cap_rank'),
                total_volume=coin_dict.get('total_volume'),
                high_24h=coin_dict.get('high_24h'),
                low_24h=coin_dict.get('low_24h'),
                price_change_24h=coin_dict.get('price_change_24h'),
                price_change_percentage_24h=coin_dict.get('price_change_percentage_24h'),
                circulating_supply=coin_dict.get('circulating_supply'),
                total_supply=coin_dict.get('total_supply'),
                max_supply=coin_dict.get('max_supply'),
                sparkline_in_7d=coin_dict.get('sparkline_in_7d')
            )
            market_data_to_add.append(market_data)
        
        # Bulk add all coins and market data
        self.coin_repository.session.add_all(coins_to_add)
        self.coin_repository.session.add_all(market_data_to_add)
        self.coin_repository.session.commit()

    def getCurrentMaketDataForUpdate(self):
        """
        Fetch current market data for all supported coins from CoinGecko.
        
        Returns:
            list[dict]: List of coin market data as dictionaries.
        """
        ids = ",".join(supported_coins)
        coin_data_list = client.coins.markets.get(
            ids=ids, 
            vs_currency=self.vs_currency, 
            per_page=250,
            precision='6'
        )

        # Convert Pydantic model objects to dicts
        market_data_dicts = []
        for coin_data in coin_data_list:
            if hasattr(coin_data, 'model_dump'):
                coin_dict = coin_data.model_dump()
            elif hasattr(coin_data, 'dict'):
                coin_dict = coin_data.dict()
            else:
                coin_dict = dict(coin_data)
            market_data_dicts.append(coin_dict)
        
        return market_data_dicts
    
    def updateCoinMarketData(self):
        """
        Fetch current market data for all supported coins and upsert records.
        Uses bulk insert with on_conflict_do_update for efficient upsert.
        """
        market_data_dicts = self.getCurrentMaketDataForUpdate()
        
        # Prepare data for bulk insert
        records = []
        for coin_dict in market_data_dicts:
            records.append({
                'coin_id': coin_dict.get('id'),
                'current_price': coin_dict.get('current_price'),
                'market_cap': coin_dict.get('market_cap'),
                'market_cap_rank': coin_dict.get('market_cap_rank'),
                'total_volume': coin_dict.get('total_volume'),
                'high_24h': coin_dict.get('high_24h'),
                'low_24h': coin_dict.get('low_24h'),
                'price_change_24h': coin_dict.get('price_change_24h'),
                'price_change_percentage_24h': coin_dict.get('price_change_percentage_24h'),
                'circulating_supply': coin_dict.get('circulating_supply'),
                'total_supply': coin_dict.get('total_supply'),
                'max_supply': coin_dict.get('max_supply'),
                'sparkline_in_7d': coin_dict.get('sparkline_in_7d'),
                'last_updated': datetime.now(timezone.utc)
            })
        
        # Bulk upsert using PostgreSQL ON CONFLICT
        stmt = insert(self.coin_repository.MarketData).values(records)
        stmt = stmt.on_conflict_do_update(
            index_elements=['coin_id'],
            set_={
                'current_price': stmt.excluded.current_price,
                'market_cap': stmt.excluded.market_cap,
                'market_cap_rank': stmt.excluded.market_cap_rank,
                'total_volume': stmt.excluded.total_volume,
                'high_24h': stmt.excluded.high_24h,
                'low_24h': stmt.excluded.low_24h,
                'price_change_24h': stmt.excluded.price_change_24h,
                'price_change_percentage_24h': stmt.excluded.price_change_percentage_24h,
                'circulating_supply': stmt.excluded.circulating_supply,
                'total_supply': stmt.excluded.total_supply,
                'max_supply': stmt.excluded.max_supply,
                'sparkline_in_7d': stmt.excluded.sparkline_in_7d,
                'last_updated': stmt.excluded.last_updated
            }
        )
        
        self.coin_repository.session.execute(stmt)
        self.coin_repository.session.commit()