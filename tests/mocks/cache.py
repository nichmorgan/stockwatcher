from functools import wraps
from unittest import mock


# We need to disable the @cache decorator during testing
def mock_cache(*args, **kwargs):
    def wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            return await func(*args, **kwargs)

        return inner

    return wrapper


mock.patch("fastapi_cache.decorator.cache", mock_cache).start()
