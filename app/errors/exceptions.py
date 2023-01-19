from fastapi import status


class APIException(Exception):
    def __init__(self, status_code: int, message: str, ex: Exception = None, detail: str = None):
        self.status_code = status_code
        self.message = message
        self.detail = detail
        self.ex = ex


class NotAuthenticatedException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="인증이 필요한 서비스 입니다.",
        )


class DuplicatedUserIdException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="이미 존재하는 아이디 입니다."
        )


class WrongPasswordException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="잘못된 아이디 또는 비밀번호입니다."
        )


class NotConfirmedUserException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="승인되지 않은 계정입니다. 관리자에게 문의해주세요."
        )


class DifferentPasswordException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="비밀번호가 서로 다릅니다. 다시 확인해주세요."
        )


class InvalidTokenException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="유효하지 않은 토큰 입니다.",
        )