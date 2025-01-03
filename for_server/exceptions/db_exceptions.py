class RegisterFailed(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class ChatBaseException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class AuthException(ChatBaseException):
    def __init__(self, message: str, status_code: int = 401):
        super().__init__(message, status_code)

class LoginFailed(AuthException):
    def __init__(self, message: str = "Failed to login."):
        super().__init__(message, status_code=401)

class ChatException(ChatBaseException):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message, status_code)

class NotParticipant(ChatException):
    def __init__(self, message: str = "Not a participant."):
        super().__init__(message, status_code=403)

class MessagePostFailed(ChatException):
    def __init__(self, message: str = "Failed to post message."):
        super().__init__(message, status_code=500)

class ChatRoomNotFound(ChatException):
    def __init__(self, message: str = "Chat room not found."):
        super().__init__(message, status_code=404)