from datetime import datetime
from django.conf import settings
from django.core.handlers import wsgi
from django.urls import set_urlconf
from django.utils.log import log_response
from structured_log import local


class WSGIRequest(wsgi.WSGIRequest):
    def __init__(self, environ):
        # Request start time
        self.start_time = datetime.now()

        # Save current request
        local.wsgi_request = self

        super().__init__(environ)


class WSGIHandler(wsgi.WSGIHandler):
    """
    Log every query but without message (for better Google Cloud log view).
    Additional information would be provided by log formater.
    """

    request_class = WSGIRequest

    def get_response(self, request):
        # Setup default url resolver for this thread
        set_urlconf(settings.ROOT_URLCONF)
        response = self._middleware_chain(request)
        response._resource_closers.append(request.close)

        if getattr(request, "user", None):
            # Django app – do not change, use default level
            level = None
        else:
            # Whitenoise (staticfiles) or something else before auth middleware
            level = "debug"

        log_response(
            "", level=level, response=response, request=request,
        )

        return response
