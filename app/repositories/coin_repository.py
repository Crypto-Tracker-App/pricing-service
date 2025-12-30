from app import db
from app.models.coinModels import Coin
from app.models.marketData import MarketData



class CoinRepository:
    """
    Thin repository providing shared database session and models.
    Services use this to access SQLAlchemy session and write queries directly.
    """
    
    # Shared session
    session = db.session
    
    # Models
    Coin = Coin
    MarketData = MarketData

