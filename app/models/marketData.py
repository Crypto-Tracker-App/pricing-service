from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import JSON
from app import db


class MarketData(db.Model):
    __tablename__ = 'market_data'
    
    coin_id = db.Column(db.String, db.ForeignKey('coins.id'), primary_key=True)
    
    # Price data
    current_price = db.Column(db.Float, nullable=False)
    market_cap = db.Column(db.BigInteger, nullable=True)
    market_cap_rank = db.Column(db.Integer, nullable=True)
    total_volume = db.Column(db.BigInteger, nullable=True)
    
    # 24h metrics
    high_24h = db.Column(db.Float, nullable=True)
    low_24h = db.Column(db.Float, nullable=True)
    price_change_24h = db.Column(db.Float, nullable=True)
    price_change_percentage_24h = db.Column(db.Float, nullable=True)
    
    # Supply info
    circulating_supply = db.Column(db.Float, nullable=True)
    total_supply = db.Column(db.Float, nullable=True)
    max_supply = db.Column(db.Float, nullable=True)
    
    # Sparkline data
    sparkline_in_7d = db.Column(JSON, nullable=True)
    
    # Timestamps
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    
    # Relationship
    coin = db.relationship('Coin', backref=db.backref('market_data', lazy=True))
    
    def __repr__(self):
        return f'<MarketData {self.coin_id} @ {self.current_price}>'
    
    def to_dict(self):
        return {
            'coin_id': self.coin_id,
            'current_price': self.current_price,
            'market_cap': self.market_cap,
            'market_cap_rank': self.market_cap_rank,
            'total_volume': self.total_volume,
            'high_24h': self.high_24h,
            'low_24h': self.low_24h,
            'price_change_24h': self.price_change_24h,
            'price_change_percentage_24h': self.price_change_percentage_24h,
            'circulating_supply': self.circulating_supply,
            'total_supply': self.total_supply,
            'max_supply': self.max_supply,
            'sparkline_in_7d': self.sparkline_in_7d,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
