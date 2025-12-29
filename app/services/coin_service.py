from app.utils.coingecko import client

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
  "fluid-usd",
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

class CoinService:
    def __init__(self, coin_repository):
        self.coin_repository = coin_repository

    def get_prices(self, coin_ids: list[str], vs_currency: str = "usd"):
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

    def fetch_and_store_prices(self, coin_ids: list[str], vs_currency: str = "usd"):
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

    def get_coin_history(self, coin_id: str, vs_currency: str = "usd", days: int | str = 7):
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
        
        pass
    