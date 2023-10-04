from . import BaseResponse


class LoginResponse(BaseResponse):
    data: dict


class RegisterResponse(BaseResponse):
    data: dict = {
        "result": {
            "id": 1,
            "user_id": "string121123",
            "name": "string",
            "birth": "2022-01-01",
            "age": 0,
            "number": -1,
            "position": "position",
            "token": "Token",
        }
    }


class DuplicateUserIdResponse(BaseResponse):
    data: dict = {"result": True}
