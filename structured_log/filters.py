import logging
from structured_log import local


class RequestInfoFilter(logging.Filter):
    def filter(self, record):
        """
        Pass request to log record
        """
        if not hasattr(record, "wsgi_request") and hasattr(local, "wsgi_request"):
            record.wsgi_request = local.wsgi_request
        return True
