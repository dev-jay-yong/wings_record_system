from fastapi import status
from pydantic import BaseModel


class BaseResponse(BaseModel):
    code: int = status.HTTP_200_OK
    message: str = "Success"
    data: list = []
