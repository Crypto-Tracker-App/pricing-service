"""Tests for pricing service API endpoints."""
import pytest
from app.models.coinModels import Coin
from app import db


class TestCoinAPI:
    """Test cases for coin API endpoints."""
    
    def test_get_top_coins_default_pagination(self, client, app):
        """Test getting top coins with default pagination."""
        with app.app_context():
            # Create test coins
            coins = [
                Coin(id='bitcoin', symbol='btc', name='Bitcoin'),
                Coin(id='ethereum', symbol='eth', name='Ethereum'),
                Coin(id='binancecoin', symbol='bnb', name='Binance Coin'),
            ]
            db.session.add_all(coins)
            db.session.commit()
        
        response = client.get('/api/top-coins')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert 'data' in data
        assert 'pagination' in data
        assert data['pagination']['limit'] == 10
        assert data['pagination']['offset'] == 0
    
    def test_get_top_coins_with_pagination(self, client, app):
        """Test getting top coins with custom pagination."""
        with app.app_context():
            # Create test coins
            coins = [Coin(id=f'coin-{i}', symbol=f'c{i}', name=f'Coin {i}') for i in range(20)]
            db.session.add_all(coins)
            db.session.commit()
        
        response = client.get('/api/top-coins?limit=5&offset=2')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert data['pagination']['limit'] == 5
        assert data['pagination']['offset'] == 2
    
    def test_get_top_coins_limit_capped_at_100(self, client, app):
        """Test that limit is capped at 100."""
        with app.app_context():
            coins = [Coin(id=f'coin-{i}', symbol=f'c{i}', name=f'Coin {i}') for i in range(10)]
            db.session.add_all(coins)
            db.session.commit()
        
        response = client.get('/api/top-coins?limit=200')
        assert response.status_code == 200
        data = response.get_json()
        assert data['pagination']['limit'] == 100
    
    def test_get_coin_ids_default_pagination(self, client, app):
        """Test getting coin IDs with default pagination."""
        with app.app_context():
            coins = [
                Coin(id='bitcoin', symbol='btc', name='Bitcoin'),
                Coin(id='ethereum', symbol='eth', name='Ethereum'),
            ]
            db.session.add_all(coins)
            db.session.commit()
        
        response = client.get('/api/coin-ids')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert isinstance(data['data'], list)
        assert 'pagination' in data
        assert data['pagination']['limit'] == 10
        assert data['pagination']['offset'] == 0
    
    def test_get_coin_ids_with_pagination(self, client, app):
        """Test getting coin IDs with custom pagination."""
        with app.app_context():
            coins = [Coin(id=f'coin-{i}', symbol=f'c{i}', name=f'Coin {i}') for i in range(15)]
            db.session.add_all(coins)
            db.session.commit()
        
        response = client.get('/api/coin-ids?limit=5&offset=3')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert data['pagination']['limit'] == 5
        assert data['pagination']['offset'] == 3
        assert isinstance(data['data'], list)
    
    def test_get_coin_ids_limit_capped_at_100(self, client, app):
        """Test that limit is capped at 100 for coin IDs."""
        with app.app_context():
            coins = [Coin(id=f'coin-{i}', symbol=f'c{i}', name=f'Coin {i}') for i in range(10)]
            db.session.add_all(coins)
            db.session.commit()
        
        response = client.get('/api/coin-ids?limit=150')
        assert response.status_code == 200
        data = response.get_json()
        assert data['pagination']['limit'] == 100
    
    def test_get_coin_by_id_success(self, client, app):
        """Test getting coin details by ID."""
        with app.app_context():
            coin = Coin(id='bitcoin', symbol='btc', name='Bitcoin')
            db.session.add(coin)
            db.session.commit()
        
        response = client.get('/api/coin/bitcoin')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert 'data' in data
    
    def test_get_coin_by_id_not_found(self, client, app):
        """Test getting coin details for non-existent coin."""
        response = client.get('/api/coin/nonexistent-coin')
        # This could return 500 or other error based on service implementation
        assert response.status_code in [404, 500]
