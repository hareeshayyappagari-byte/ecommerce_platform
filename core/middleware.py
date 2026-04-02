import logging

from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('ecommerce')


class ExceptionLoggingMiddleware(MiddlewareMixin):
    """Middleware for logging uncaught exceptions with traceback."""

    def process_exception(self, request: HttpRequest, exception: Exception) -> HttpResponse | None:  # type: ignore[name-defined]
        logger.error(
            'Unhandled exception during request %s %s',
            request.method,
            request.path,
            exc_info=exception,
        )
        return None
