from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.routers.response_model.user_response import *
from app.routers.requests_model.user_requests import *
from app.services.user_service import User

router = APIRouter(prefix="/user", tags=["user"])
user_class = User()


@router.post(
    path="/register",
    response_model=RegisterResponse,
)
async def register_user(register_request_model: RegisterRequestModel) -> dict:
    """
    ```identifier```: 회원가입 할 아이디 <br>
    ```password```: 회원가입 할 비밀번호 <br>
    ```password_check```: 회원가입 할 비밀번호 한 번 더 입력 (확인용) <br>
    ```name```: 본인 실명 <br>
    ```birth_day```: 본인 생일 (%Y-%m-%d 형식) <br>
    ```age```: 본인 나이 <br>
    ```number```: 본인 배구 등 번호 (없는 경우 null) <br>
    ```position```: 본인 배구 포지션 (아포짓 스파이커, 아웃사이드 히터, 세터, 미들 블로커, 리베로 중 택 1) <br>
    """

    result = user_class.register_user(register_request_model)
    return {"data": {"result": result}}


@router.get(
    path="/check-duplicate",
    response_model=DuplicateUserIdResponse,
)
async def login_user(user_id: str) -> dict:
    """
    ```user_id```: 회원가입 할 아이디 (query param) <br>

    return : 이미 존재하는 아이디면 True 회원 가입이 가능한 아이디면 False 반환
    """

    result = user_class.check_duplicate_user_id(user_id)

    return {"data": {"result": result}}


@router.post(
    path="/login",
    response_model=DuplicateUserIdResponse,
)
async def login_user(login_request_model: LoginRequestModel) -> dict:
    """
    ```user_id```: 회원가입 할 아이디 (query param) <br>

    return : 이미 존재하는 아이디면 True 회원 가입이 가능한 아이디면 False 반환
    """

    result = user_class.login_user(login_request_model.user_id, login_request_model.password)

    return {"data": {"result": result}}
