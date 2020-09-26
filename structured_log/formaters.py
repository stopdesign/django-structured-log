import json
import logging
from datetime import datetime
from django.conf import settings
from django.utils.encoding import iri_to_uri, escape_uri_path


class GoogleCloudFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        """Returns JSON formatted to fit Google Cloud Run log streams.
        To assist log event grouping, the Cloud Trace header
        is parsed and a project-specific logging trace is added.
        """

        request = getattr(record, "wsgi_request", None)
        request_meta = request.META if request else None
        response = getattr(record, "response", None) or {}
        response_size = getattr(record, "length", None)
        status_code = getattr(record, "status_code", None)

        event = {
            "severity": record.levelname,
            "module": record.module,
            "logger": record.name,
            "function": record.funcName,
            "lineno": record.lineno,
            "pathname": record.pathname,
        }

        # Auth User
        if request and hasattr(request, "user") and request.user:
            event["user"] = request.user

        # Get message only for custom log events
        if record.getMessage() and not getattr(record, "exc_info", None):
            if record.name != "django.request":
                event["message"] = record.getMessage()

        if request_meta:
            # Full request URI
            request_url = escape_uri_path(request_meta.get("PATH_INFO"))
            if request_meta.get("QUERY_STRING", ""):
                request_url += "?" + iri_to_uri(request_meta.get("QUERY_STRING", ""))

            event["httpRequest"] = {
                "requestMethod": request_meta.get("REQUEST_METHOD", ""),
                "userAgent": request_meta.get("HTTP_USER_AGENT", ""),
                "remoteIp": request_meta.get("REMOTE_ADDR", ""),
                "referer": request_meta.get("HTTP_REFERER", ""),
                "protocol": request_meta.get("SERVER_PROTOCOL", ""),
            }

            # RequestUrl has a higher priority,
            # so only add it when there is no message.
            if "message" not in event:
                event["httpRequest"]["requestUrl"] = request_url

            # Content length
            if response_size:
                event["httpRequest"]["responseSize"] = response_size

            # Status code
            if response.get("status_code"):
                event["httpRequest"]["status"] = response.get("status_code")
            elif status_code:
                event["httpRequest"]["status"] = status_code

            # Latency
            if hasattr(request, "start_time"):
                dt = datetime.now() - getattr(request, "start_time")
                event["httpRequest"]["latency"] = {
                    "seconds": dt.seconds,
                    "nanos": dt.microseconds * 1000,
                }

            event["X-Forwarded-For"] = request_meta.get("HTTP_X_FORWARDED_FOR")

            # Cloud Run Trace ID
            project_id = getattr(settings, "PROJECT_ID", None)
            if project_id:
                trace_header = request_meta.get("HTTP_X_CLOUD_TRACE_CONTEXT")
                trace_id = trace_header.split("/")[0]
                trace = "projects/%s/traces/%s" % (project_id, trace_id)
                event["logging.googleapis.com/trace"] = trace

        if record.exc_info:
            event["exception"] = self.formatException(record.exc_info)

        return json.dumps(event, default=str, ensure_ascii=False)
