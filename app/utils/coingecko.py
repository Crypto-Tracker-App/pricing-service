from coingecko_sdk import Coingecko
from app.config import Config

client = Coingecko(
    demo_api_key = Config.COINGEKO_API_KEY,
    environment = "demo",
)