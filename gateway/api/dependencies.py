from gateway.services.gateway_service import GatewayService


def get_gateway_service() -> GatewayService:
    """
    Returns the Gateway Service instance.

    Later we can inject configuration,
    database connections,
    cache,
    or authentication here.
    """
    return GatewayService()