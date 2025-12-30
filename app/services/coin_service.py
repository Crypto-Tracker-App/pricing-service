from datetime import datetime, timezone
from sqlalchemy import insert
from app.utils.coingecko import client
from app.repositories.coin_repository import CoinRepository
from app.models.coinModels import supported_coins

class CoinService:
    def __init__(self, coin_repository: CoinRepository, vs_currency: str = "eur"):
        self.coin_repository = coin_repository
        self.vs_currency = vs_currency

    def get_prices(self, coin_ids: list[str], vs_currency: str = "eur"):
        """
        Fetch current prices for the given coin IDs using CoinGecko.
        Returns the raw response dict from the SDK.
        """
        ids = ",".join(coin_ids)
        return client.simple.price.get(
            ids=ids,
            vs_currencies=vs_currency,
            include_24hr_change=True,
            include_last_updated_at=True,
        )

    def fetch_and_store_prices(self, coin_ids: list[str], vs_currency: str = "eur"):
        """
        Fetch current prices and persist them via the repository.
        Returns the fetched response.
        """
        ids = ",".join(coin_ids)
        response = client.simple_price(
            ids=ids,
            vs_currencies=vs_currency,
            include_24hr_change=True,
            include_last_updated_at=True,
        )
        # Persist via repository (simple implementation may be a no-op)
        self.coin_repository.save_prices(response, vs_currency)
        return response

    # FIXME: FIX THIS
    def get_coin_history(self, coin_id: str, vs_currency: str = "eur", days: int | str = 7):
        """
        Fetch historical market chart data for a coin.
        Returns the raw response dict from the SDK.
        """
        return client.coins_id_market_chart(
            id=coin_id,
            vs_currency=vs_currency,
            days=str(days),
        )
    
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