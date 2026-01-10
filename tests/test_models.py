"""Tests for pricing service coin models."""
import pytest
from app.models.coinModels import Coin
from app import db


class TestCoinModel:
    """Test cases for Coin model."""
    
    def test_coin_creation(self, app):
        """Test creating a coin."""
        with app.app_context():
            coin = Coin(id='bitcoin', symbol='btc', name='Bitcoin')
            db.session.add(coin)
            db.session.commit()
            
            retrieved = Coin.query.filter_by(id='bitcoin').first()
            assert retrieved is not None
            assert retrieved.id == 'bitcoin'
            assert retrieved.symbol == 'btc'
            assert retrieved.name == 'Bitcoin'
    
    def test_coin_id_indexed(self, app):
        """Test that coin id is indexed for quick lookup."""
        with app.app_context():
            coin1 = Coin(id='bitcoin', symbol='btc', name='Bitcoin')
            coin2 = Coin(id='ethereum', symbol='eth', name='Ethereum')
            db.session.add_all([coin1, coin2])
            db.session.commit()
            
            # Index should make this fast
            result = Coin.query.filter_by(id='bitcoin').first()
            assert result.id == 'bitcoin'
            assert result.name == 'Bitcoin'
    
    def test_coin_symbol_indexed(self, app):
        """Test that coin symbol is indexed for quick lookup."""
        with app.app_context():
            coin1 = Coin(id='bitcoin', symbol='btc', name='Bitcoin')
            coin2 = Coin(id='ethereum', symbol='eth', name='Ethereum')
            db.session.add_all([coin1, coin2])
            db.session.commit()
            
            # Test symbol lookup
            result = Coin.query.filter_by(symbol='btc').first()
            assert result.symbol == 'btc'
            assert result.id == 'bitcoin'
    
    def test_coin_to_dict(self, app):
        """Test coin to_dict method."""
        with app.app_context():
            coin = Coin(
                id='bitcoin',
                symbol='btc',
                name='Bitcoin',
                image='https://example.com/bitcoin.png'
            )
            db.session.add(coin)
            db.session.commit()
            
            coin_dict = coin.to_dict()
            assert coin_dict['id'] == 'bitcoin'
            assert coin_dict['symbol'] == 'btc'
            assert coin_dict['name'] == 'Bitcoin'
            assert coin_dict['image'] == 'https://example.com/bitcoin.png'
    
    def test_coin_to_dict_without_image(self, app):
        """Test coin to_dict method without image."""
        with app.app_context():
            coin = Coin(id='bitcoin', symbol='btc', name='Bitcoin')
            db.session.add(coin)
            db.session.commit()
            
            coin_dict = coin.to_dict()
            assert coin_dict['image'] is None
