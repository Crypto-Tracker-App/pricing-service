"""Service for triggering alerts in alert-service with resilience."""

import requests
import logging
import os
from app.utils.resilience import retry, circuit_breaker

logger = logging.getLogger(__name__)


@retry(max_attempts=3, delay=1)
@circuit_breaker(failure_threshold=5, recovery_timeout=60, name="alert_service")
def trigger_alert_check() -> bool:
    """
    Trigger alert checking in alert-service with resilience.
    
    Returns:
        True if successful, False otherwise
    """
    alert_service_url = os.getenv('ALERT_SERVICE_URL', 'http://alert-service:5000')
    check_alerts_url = f"{alert_service_url}/api/check-alerts"
    
    try:
        response = requests.post(check_alerts_url, timeout=5)
        response.raise_for_status()
        logger.info("Alert check triggered successfully!", extra={"url": check_alerts_url})
        return True
    except requests.exceptions.Timeout:
        logger.error(f"Timeout triggering alert check at {check_alerts_url}")
        raise
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error triggering alert check: {str(e)}")
        raise
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to trigger alert check: {e}", extra={"url": check_alerts_url})
        raise
