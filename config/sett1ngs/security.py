from .base import *

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
    ALLOWED_HOSTS = ["*"]
    INTERNAL_IPS = [
        "127.0.0.1",
    ]
    CSRF_TRUSTED_ORIGINS = [
        "https://apitest.fpna.ir",
    ]
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
else:
    CORS_ALLOWED_ORIGINS = [
        "https://apitest.fpna.ir",
    ]
    ALLOWED_HOSTS = [
        "apitest.fpna.ir",
    ]
    INTERNAL_IPS = []
    SECURE_HSTS_SECONDS = 31536000  # 1 year in seconds
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

CORS_ALLOW_CREDENTIALS = False

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
