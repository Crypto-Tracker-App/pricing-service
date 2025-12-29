from typing import Dict, Any

from app.utils.logger import get_logger

logger = get_logger(__name__)


class CoinRepository:
    """
    Simple repository abstraction for coin-related persistence.
    Currently a minimal implementation that logs operations.
    Can be extended to use SQLAlchemy models for real persistence.
    """

    def save_prices(self, prices: Dict[str, Any], vs_currency: str) -> None:
        """
        Persist fetched prices.
        This minimal implementation just logs; replace with DB writes as needed.
        """
        # Example structure: { "bitcoin": {"usd": 12345.67, ...}, ... }
        try:
            total = len(prices) if isinstance(prices, dict) else 0
            logger.info(
                "Saving prices (stub)",
                extra={"count": total, "vs_currency": vs_currency},
            )
            # TODO: Implement SQLAlchemy models and persist here.
        except Exception as e:
            logger.error(f"Failed to save prices: {e}", exc_info=True)
            raise
