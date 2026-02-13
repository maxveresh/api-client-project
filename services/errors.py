class UserNotFound(Exception):
    pass

class UserServiceUnavailable(Exception):
    pass

class UserAlreadyExists(Exception):
    pass

class InvalidUserData(Exception):
    pass

class AuthServiceUnavailable(Exception):
    pass

class InvalidCredentials(Exception):
    pass

class TokenExpired(Exception):
    pass