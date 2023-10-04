from fastapi import status


class APIException(Exception):
    def __init__(
        self, status_code: int, message: str, ex: Exception = None, detail: str = None
    ):
        self.status_code = status_code
        self.message = message
        self.detail = detail
        self.ex = ex


class TokenExpiredEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=f"세션이 만료되어 로그아웃 되었습니다.",
            detail="Token Expired",
            ex=ex,
        )


class InvalidTokenEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=f"잘못된 토큰입니다.",
            detail="Invalid Token",
            ex=ex,
        )


class TokenDecodeEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=f"비정상적인 접근입니다.",
            detail="Token has been compromised.",
            ex=ex,
        )


class NotAuthenticatedException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="인증이 필요한 서비스 입니다.",
        )


class DuplicatedUserIdException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, message="이미 존재하는 아이디 입니다."
        )


class WrongPasswordException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, message="잘못된 아이디 또는 비밀번호입니다."
        )


class NotConfirmedUserException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="승인되지 않은 계정입니다. 관리자에게 문의해주세요.",
        )


class NotExistCoachException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, message="해당 팀에 코치가 존재하지 않습니다."
        )


class TeamNotFoundException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, message="조회하려는 팀이 존재하지 않습니다."
        )


class DifferentPasswordException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="비밀번호가 서로 다릅니다. 다시 확인해주세요.",
        )


class InvalidPositionException(APIException):
    def __init__(self, position_name: str = None) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="포지션 정보가 잘못 되었습니다. 다시 확인해주세요.",
            detail=f"입력 가능한 포지션 - ['아웃사이드 히터', '아포짓 스파이커', '미들 블로커', '세터', '리베로'] | 입력한 포지션 : {position_name}",
        )


class InvalidTokenException(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="유효하지 않은 토큰 입니다.",
        )
