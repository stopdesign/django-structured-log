import threading

import django.utils.log

from .wsgi import get_wsgi_application

local = threading.local()

__all__ = ["local", "get_wsgi_application"]


# Add content length to log records
def log_response_cor(
    message,
    *args,
    response=None,
    request=None,
    logger=django.utils.log.request_logger,
    level=None,
    exception=None,
):  
    if getattr(response, "_has_been_logged", False):
        return

    if level is None:
        if response.status_code >= 500:
            level = "error"
        elif response.status_code >= 400:
            level = "warning"
        else:
            level = "info"

    getattr(logger, level)(
        message,
        exception,
        *args,
        extra={
            "length": len(response.content) if hasattr(response, "content") else None,
            "status_code": response.status_code,
            "request": request,
        },
        exc_info=(
            type(exception), exception, getattr(exception, "__traceback__", None)
        ),
    )
    response._has_been_logged = True


# Patch log_response
django.utils.log.log_response = log_response_cor
