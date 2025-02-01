from fastapi import HTTPException


class AuthenticationError(HTTPException):
    def __init__(self, detail: str = "Login or password is not valid", status_code: int = 403):
        super().__init__(status_code=status_code, detail=detail)