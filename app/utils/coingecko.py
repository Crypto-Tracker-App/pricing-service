from coingecko_sdk import Coingecko
from app.config import Config

client = Coingecko(
    demo_api_key = Config.COINGECKO_API_KEY,
    environment = "demo",
)