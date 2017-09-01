import time
from functools import wraps
from mercadolibre.exceptions import TokenExpired


def valid_token(func):
    @wraps(func)
    def helper(*args, **kwargs):
        client = args[0]
        if client.expires_at and not client.expires_at > time.time():
            raise TokenExpired('You must refresh the token.')
        return func(*args, **kwargs)

    return helper
