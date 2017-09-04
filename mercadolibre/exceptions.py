class BaseError(Exception):
    pass


class InvalidSite(BaseError):
    pass


class TokenExpired(BaseError):
    pass


class InvalidPictureParameter(BaseError):
    pass
