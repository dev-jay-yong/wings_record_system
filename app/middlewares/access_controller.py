import base64
import hmac
import time
import typing
import re
import tomllib

import jwt

from jwt.exceptions import ExpiredSignatureError, DecodeError
from starlette.requests import Request
from starlette.responses import JSONResponse

# from app.database.conn import db
# from app.database.schema import Users, ApiKeys
from app.errors import exceptions as ex
from app.errors.exceptions import APIException
from app.utils.logger import api_logger
from app.utils.util import query_to_dict, DateTimeHandler

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

    ip = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers.keys() else request.client.host
    request.state.ip = ip.split(",")[0] if "," in ip else ip
    headers = request.headers
    cookies = request.cookies

    # url = request.url.path
    # if await url_pattern_check(url, path_setting['EXCEPT_PATH_REGEX']) or url in path_setting['EXCEPT_PATH_LIST']:
    #     response = await call_next(request)
    #     if url != "/":
    #         await api_logger(request=request, response=response)
    #     return response

    try:
        qs = str(request.query_params)
        qs_list = qs.split("&")
        # session = next(db.session())
        # try:
        #     qs_dict = {qs_split.split("=")[0]: qs_split.split("=")[1] for qs_split in qs_list}
        # except Exception:
        #     raise ex.APIQueryStringEx()

        # api_key = ApiKeys.get(session=session, access_key=qs_dict["key"])

        # now_timestamp = int(DateTimeHandler.datetime(diff=9).timestamp())
        # if now_timestamp - 10 > int(qs_dict["timestamp"]) or now_timestamp < int(qs_dict["timestamp"]):
        #     raise ex.APITimestampEx()

        user_info = "user_data"
        request.state.user = user_info
        response = await call_next(request)
        await api_logger(request=request, response=response)
    except Exception as e:

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
