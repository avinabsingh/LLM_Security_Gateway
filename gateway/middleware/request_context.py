import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from gateway.core.logger import logger


class RequestContextMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        request_id = str(uuid.uuid4())

        start_time = time.perf_counter()

        request.state.request_id = request_id

        logger.info(
            f"[{request_id}] Incoming {request.method} {request.url.path}"
        )

        response = await call_next(request)

        latency = (time.perf_counter() - start_time) * 1000

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time"] = f"{latency:.2f} ms"

        logger.info(
            f"[{request_id}] "
            f"Completed {response.status_code} "
            f"in {latency:.2f} ms"
        )

        return response