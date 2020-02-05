class BaseError(Exception):
    def __init__(self, message, status_code):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code


class AuthError(BaseError):
    def __init__(self):
        BaseError.__init__(self, 'Auth Error', 401)

