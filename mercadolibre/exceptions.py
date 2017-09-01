class BaseError(Exception):
    pass


class InvalidSite(BaseError):
    pass


class TokenExpired(BaseError):
    pass
