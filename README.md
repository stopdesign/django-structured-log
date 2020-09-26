## Structured log for Django in Google Cloud Run

![Usage example](https://raw.githubusercontent.com/stopdesign/django-structured-log/master/img/example.png)

### Add structured_log to INSTALLED_APPS
```.python
INSTALLED_APPS = [
    ...
    "structured_log",
    ...
]
```

### Update logging settings
Add filter, formater and handler. Use handler for logging.
```.python
"filters": {
    "request_info": {
        "()": "structured_log.filters.RequestInfoFilter"
    }
},
"formatters": {
    "cloudrun": {
        "()": "structured_log.formaters.GoogleCloudFormatter"
    },
},
"handlers": {
    "console": {
        "level": "DEBUG",
        "class": "logging.StreamHandler",
        "stream": sys.stdout,
        "formatter": "cloudrun",
        "filters": ["request_info"],
    },
},
"loggers": {
    "": {
        "level": "INFO",
        "handlers": ["console"],
        "propagate": False
    },
    "django": {
        "level": "INFO",
        "handlers": ["console"],
        "propagate": False
    },
    ...
}
```

### WSGIHandler
Replace get_wsgi_application import in wsgi.py.
```.python
import os

from structured_log import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

application = WSGIHandler()
```

### [OPTIONAL] Client IP address
Use `django-xff` to set HTTP_REMOTE_ADDR from X-Forwarded-For header.
```.python
MIDDLEWARE = [
    "xff.middleware.XForwardedForMiddleware",
    ...
]

# Only one proxy for Cloud Run
XFF_TRUSTED_PROXY_DEPTH = 1
```
