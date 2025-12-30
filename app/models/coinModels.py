from typing import Optional
from pydantic import BaseModel
from app import db


class CoinMarketData(BaseModel):
    """
    Pydantic model for coin data from CoinGecko markets API.
    Provides type hints and IDE autocomplete suggestions.
    """
    id: Optional[str] = None
    symbol: Optional[str] = None
    name: Optional[str] = None
    image: Optional[str] = None
    current_price: Optional[float] = None
    market_cap: Optional[int] = None
    market_cap_rank: Optional[int] = None
    fully_diluted_valuation: Optional[int] = None
    total_volume: Optional[int] = None
    high_24h: Optional[float] = None
    low_24h: Optional[float] = None
    price_change_24h: Optional[float] = None
    price_change_percentage_24h: Optional[float] = None
    market_cap_change_24h: Optional[int] = None
    market_cap_change_percentage_24h: Optional[float] = None
    circulating_supply: Optional[float] = None
    total_supply: Optional[float] = None
    max_supply: Optional[float] = None
    ath: Optional[float] = None
    ath_change_percentage: Optional[float] = None
    ath_date: Optional[str] = None
    atl: Optional[float] = None
    atl_change_percentage: Optional[float] = None
    atl_date: Optional[str] = None
    roi: Optional[str] = None
    last_updated: Optional[str] = None
    
    class Config:
        from_attributes = True


class Coin(db.Model):
    __tablename__ = 'coins'
    
    id = db.Column(db.String, primary_key=True)
    symbol = db.Column(db.String(8), nullable=False)
    name = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=True)
    
    def __repr__(self):
        return f'<Coin {self.id} ({self.symbol})>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'name': self.name,
            'image': self.image
        }



supported_coins = [
  "bitcoin",
  "ethereum",
  "tether",
  "binancecoin",
  "ripple",
  "usd-coin",
  "solana",
  "tron",
  "dogecoin",
  "cardano",
  "bitcoin-cash",
  "usds",
  "chainlink",
  "zcash",
  "monero",
  "hyperliquid",
  "stellar",
  "ethena-usde",
  "litecoin",
  "avalanche-2",
  "dai",
  "whitebit",
  "canton-network",
  "hedera-hashgraph",
  "shibacoin",
  "the-open-network",
  "world-liberty-financial",
  "uniswap",
  "paypal-usd",
  "crypto-com-chain",
  "ethena-staked-usde",
  "mantle",
  "stupid-world-liberty-financial",
  "polkadot",
  "memecore",
  "bitget-token",
  "bittensor",
  "aave",
  "okb",
  "fluid-usdc",
  "near",
  "ethereum-classic",
  "asterion",
  "pepe",
  "pi-network",
  "tether-gold",
  "ethena",
  "internet-computer",
  "midnight",
  "pax-gold",
  "global-dollar",
  "sky",
  "kucoin-shares",
  "RLUripple-usdSD",
  "worldcoin-wld",
  "aptos",
  "ondo-finance",
  "kaspa",
  "polygon-ecosystem-token",
  "arbitrum",
  "algorand",
  "official-trump",
  "filecoin",
  "cosmos",
  "vechain",
  "solv-btc",
  "xdce-crowd-sale",
  "Llombard-staked-btcBTC",
  "myx-finance",
  "flare-networks",
  "quant-network",
  "gatechain-token",
  "sei-network",
  "beldex",
  "render-token",
  "bonk",
  "loaded-lions",
  "pancakeswap-token",
  "jupiter",
  "pump",
  "nexo",
  "pudgy-penguins",
  "curve-dao-token",
  "story-2",
  "lombard-protocol",
  "tezos",
  "dash",
  "optimism",
  "usdd",
  "first-digital-usd",
  "evervalue-coin",
  "fetch-ai",
  "gho",
  "true-usd",
  "kite",
  "audiera",
  "blockstack",
  "injective-protocol",
  "newton-project",
  "immutable-x"
]