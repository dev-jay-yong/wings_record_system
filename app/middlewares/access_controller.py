import base64
import hmac
import time
import traceback
import typing
import re
import tomllib

import jwt

from jwt.exceptions import ExpiredSignatureError, DecodeError
from starlette.requests import Request
from starlette.responses import JSONResponse

from models.base import db
from models.user_model import UserHelper
from errors import exceptions as ex
from errors.exceptions import APIException
from utils.logger import api_logger
from utils.util import query_to_dict, DateTimeHandler

with open("app/common/setting.toml", "rb") as f:
    setting_dict = tomllib.load(f)

path_setting = setting_dict['PATH_SETTING']
security_setting = setting_dict['SECURITY_SETTING']


async def access_control(request: Request, call_next):
    request.state.req_time = DateTimeHandler.datetime()
    request.state.start = time.time()
    request.state.inspect = None
    request.state.user = None
    request.state.service = None
    user_helper = UserHelper()

    ip = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers.keys() else request.client.host
    request.state.ip = ip.split(",")[0] if "," in ip else ip
    headers = request.headers
    cookies = request.cookies

    url = request.url.path

    try:
        db.connect(reuse_if_open=True)
        if await url_pattern_check(url, path_setting['EXCEPT_PATH_REGEX']) or url in path_setting['EXCEPT_PATH_LIST']:
            response = await call_next(request)
            if url != "/":
                await api_logger(request=request, response=response)
            return response

        if headers.get("Authorization") is None:
            raise ex.NotAuthenticatedException()

        token_info = await token_decode(access_token=headers.get("Authorization"))
        request.state.user = user_helper.get_one_user_by_id(token_info['user_id'], is_dict=False)

        if request.state.user is None:
            raise ex.TokenDecodeEx()

        if request.state.user.confirm is False:
            raise ex.NotConfirmedUserException()

        response = await call_next(request)
        await api_logger(request=request, response=response)
    except Exception as e:
        print(traceback.format_exception(e))

        error = await exception_handler(e)
        error_dict = dict(message=error.message, detail=error.detail, status_code=error.status_code)
        response = JSONResponse(status_code=error.status_code, content=error_dict)
        await api_logger(request=request, error=error)

    return response


async def url_pattern_check(path, pattern):
    result = re.match(pattern, path)
    if result:
        return True
    return False


async def token_decode(access_token):
    """
    :param access_token:
    :return:
    """
    try:
        access_token = access_token.replace("Bearer ", "")
        payload = jwt.decode(access_token, key=security_setting['JWT_SECRET'],
                             algorithms=[security_setting['JWT_ALGORITHM']])
    except ExpiredSignatureError:
        raise ex.TokenExpiredEx()
    except DecodeError:
        raise ex.TokenDecodeEx()
    return payload


async def exception_handler(error: Exception):
    print(error)
    if not isinstance(error, APIException):
        error = APIException(ex=error,
                             message="일시적인 오류가 발생하였습니다. 다시 시도해 주세요.",
                             detail=str(error), status_code=500)
    return error
