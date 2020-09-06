from rest_framework import status
from rest_framework_json_api.exceptions import (
    exception_handler as drf_json_api_exception_handler,
)

from .proxies.exceptions import ExchangeProxyException


def exception_handler(exc, context):
    if isinstance(exc, ExchangeProxyException):
        exc.status_code = status.HTTP_424_FAILED_DEPENDENCY
    return drf_json_api_exception_handler(exc, context)
