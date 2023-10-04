import secrets
from typing import Optional

import requests
from fastapi import Response, Request, APIRouter, Depends, HTTPException, Header, Query
from fastapi.responses import RedirectResponse
from starlette import status

from routers.response_model.user_response import *
from routers.requests_model.user_requests import *
from services.user_service import User
from utils.oauth_client import OAuthClient

router = APIRouter(prefix="/user", tags=["user"])
user_class = User()


kakao_client = OAuthClient(
    client_id="bd9b741a1e606cc77952dee9989fedd2",
    client_secret_id="bd9b741a1e606cc77952dee9989fedd2",
    redirect_uri="http://127.0.0.1:8000/user/callback",
    authentication_uri="https://kauth.kakao.com/oauth",
    resource_uri="https://kapi.kakao.com/v2/user/me",
    verify_uri="https://kapi.kakao.com/v1/user/access_token_info",
)


def get_oauth_client(provider: str = Query("kakao", regex="naver|kakao")):
    if provider == "kakao":
        return kakao_client


def get_authorization_token(authorization: str = Header(...)) -> str:
    scheme, _, param = authorization.partition(" ")
    if not authorization or scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return param


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
async def check_duplicate(user_id: str) -> dict:
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

    result = user_class.login_user(
        login_request_model.user_id, login_request_model.password
    )

    return {"data": {"result": result}}


@router.get("/kakao-login")
async def kakao_login(oauth_client=Depends(get_oauth_client)):
    state = secrets.token_urlsafe(32)
    login_url = oauth_client.get_oauth_login_url(state=state)
    return RedirectResponse(login_url)


@router.get("/callback")
async def callback(
    code: str, state: Optional[str] = None, oauth_client=Depends(get_oauth_client)
):
    token_response = await oauth_client.get_tokens(code, state)

    return {"response": token_response}


@router.get("/refresh")
async def refresh(
    oauth_client=Depends(get_oauth_client),
    refresh_token: str = Depends(get_authorization_token),
):
    token_response = await oauth_client.refresh_access_token(
        refresh_token=refresh_token
    )

    return {"response": token_response}


@router.get("/user", dependencies=[Depends(get_oauth_client)])
async def get_user(
    oauth_client=Depends(get_oauth_client),
    access_token: str = Depends(get_authorization_token),
):
    user_info = await oauth_client.get_user_info(access_token=access_token)
    return {"user": user_info}
