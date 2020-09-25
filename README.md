https://github.com/stopdesign/django-structured-log/{current-commit-id}/README.md

https://raw.githubusercontent.com/stopdesign/django-structured-log/{current-commit-id}/img/example.png

![Usage example](https://raw.githubusercontent.com/stopdesign/django-structured-log/{current-commit-id}/img/example.png)

![Usage example 1](https://raw.githubusercontent.com/stopdesign/django-structured-log/master/img/example.png)

### Add cloudrun_log to INSTALLED_APPS
```.python
INSTALLED_APPS = [
    ...
    "cloudrun_log",
    ...
]
```

### Update logging settings
Add filter, formater and handler. Use handler for logging.
```.python
"filters": {
    "request_info": {
        "()": "cloudrun_log.filters.RequestInfoFilter"
    }
},
"formatters": {
    "cloudrun": {
        "()": "cloudrun_log.formaters.GoogleCloudFormatter"
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
Replace WSGIHandler in wsgi.py.
```.python
import os
import django
from cloudrun_log.request_handler import WSGIHandler

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

django.setup(set_prefix=False)
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
