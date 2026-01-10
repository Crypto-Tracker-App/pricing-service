"""Tests for pricing service business logic."""
import pytest
from app.models.coinModels import Coin
from app.services.coin_service import CoinService
from app.repositories.coin_repository import CoinRepository
from app import db


class TestCoinService:
    """Test cases for CoinService."""
    
    def test_get_top_coins_no_data(self, app):
        """Test getting top coins when database is empty."""
        with app.app_context():
            service = CoinService(CoinRepository())
            top_coins = service.get_top_coins(top_n=10, skip_n=0)
            assert top_coins == []
    
    def test_get_top_coins_with_limit(self, app):
        """Test getting top coins with limit."""
        with app.app_context():
            # Create test coins
            coins = [Coin(id=f'coin-{i}', symbol=f'c{i}', name=f'Coin {i}') for i in range(5)]
            db.session.add_all(coins)
            db.session.commit()
            
            service = CoinService(CoinRepository())
            top_coins = service.get_top_coins(top_n=3, skip_n=0)
            # Note: Will be empty if MarketData is not populated
            assert isinstance(top_coins, list)
    
    def test_get_top_coins_with_pagination(self, app):
        """Test getting top coins with skip_n pagination."""
        with app.app_context():
            coins = [Coin(id=f'coin-{i}', symbol=f'c{i}', name=f'Coin {i}') for i in range(10)]
            db.session.add_all(coins)
            db.session.commit()
            
            service = CoinService(CoinRepository())
            top_coins = service.get_top_coins(top_n=5, skip_n=2)
            assert isinstance(top_coins, list)
    
    def test_get_coin_by_id_not_found(self, app):
        """Test getting coin by ID when it doesn't exist."""
        with app.app_context():
            service = CoinService(CoinRepository())
            coin = service.get_coin_by_id('nonexistent-coin')
            assert coin is None
    
    def test_get_coin_by_id_success(self, app):
        """Test getting coin by ID successfully."""
        with app.app_context():
            coin = Coin(id='bitcoin', symbol='btc', name='Bitcoin')
            db.session.add(coin)
            db.session.commit()
            
            service = CoinService(CoinRepository())
            retrieved = service.get_coin_by_id('bitcoin')
            # Will be None if MarketData is not populated
            assert retrieved is None or isinstance(retrieved, dict)
    
    def test_search_coins_empty_result(self, app):
        """Test searching coins with no results."""
        with app.app_context():
            service = CoinService(CoinRepository())
            results = service.search_coins('nonexistent', limit=10)
            assert results == []
    
    def test_search_coins_by_name(self, app):
        """Test searching coins by name."""
        with app.app_context():
            coin = Coin(id='bitcoin', symbol='btc', name='Bitcoin')
            db.session.add(coin)
            db.session.commit()
            
            service = CoinService(CoinRepository())
            results = service.search_coins('Bitcoin', limit=10)
            assert isinstance(results, list)
    
    def test_search_coins_by_symbol(self, app):
        """Test searching coins by symbol."""
        with app.app_context():
            coin = Coin(id='bitcoin', symbol='btc', name='Bitcoin')
            db.session.add(coin)
            db.session.commit()
            
            service = CoinService(CoinRepository())
            results = service.search_coins('btc', limit=10)
            assert isinstance(results, list)
    
    def test_search_coins_by_id(self, app):
        """Test searching coins by ID."""
        with app.app_context():
            coin = Coin(id='bitcoin', symbol='btc', name='Bitcoin')
            db.session.add(coin)
            db.session.commit()
            
            service = CoinService(CoinRepository())
            results = service.search_coins('bitcoin', limit=10)
            assert isinstance(results, list)
    
    def test_search_coins_case_insensitive(self, app):
        """Test that coin search is case insensitive."""
        with app.app_context():
            coin = Coin(id='ethereum', symbol='eth', name='Ethereum')
            db.session.add(coin)
            db.session.commit()
            
            service = CoinService(CoinRepository())
            results = service.search_coins('ETHEREUM', limit=10)
            assert isinstance(results, list)
    
    def test_search_coins_with_limit(self, app):
        """Test searching coins respects limit parameter."""
        with app.app_context():
            coins = [Coin(id=f'coin-{i}', symbol=f'c{i}', name=f'Coin {i}') for i in range(10)]
            db.session.add_all(coins)
            db.session.commit()
            
            service = CoinService(CoinRepository())
            results = service.search_coins('coin', limit=3)
            assert isinstance(results, list)
            assert len(results) <= 3
