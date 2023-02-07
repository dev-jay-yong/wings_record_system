import tomllib

import jwt
from playhouse.shortcuts import model_to_dict

from models.user_model import UserHelper
from errors import exceptions as ex

import bcrypt


class User:
    def __init__(self):
        self.user_helper = UserHelper()

    def check_duplicate_user_id(self, user_id):
        exist_user = self.user_helper.get_one_user_by_id(user_id)

        return bool(exist_user)

    def login_user(self, user_id, password):
        user = self.user_helper.get_one_user_by_id(user_id, is_dict=True)

        print(user['password'], password.encode('utf-8'))
        if user is None or bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')) is False:
            raise ex.WrongPasswordException()

        if not user['confirm']:
            raise ex.NotConfirmedUserException()

        user.pop('password')

        return user

    def register_user(self, register_data):
        # todo: 조회할 때 로우 존재 여부만 count로 조회 하도록 변경
        exist_user = self.user_helper.get_one_user_by_id(register_data.identifier)

        if exist_user is not None:
            raise ex.DuplicatedUserIdException()

        if register_data.password != register_data.password_check:
            raise ex.DifferentPasswordException()

        position_info = self.user_helper.get_position_by_name(register_data.position)

        if position_info is None:
            raise ex.InvalidPositionException(register_data.position)

        register_data.password = bcrypt.hashpw(password=register_data.password.encode('utf-8'), salt=bcrypt.gensalt())
        register_data = register_data.__dict__

        with open("app/common/setting.toml", "rb") as f:
            security_setting = tomllib.load(f)['SECURITY_SETTING']

        register_data['token'] = jwt.encode({'user_id': register_data['identifier']},
                                            security_setting['JWT_SECRET'],
                                            security_setting['JWT_ALGORITHM'])
        register_data['position'] = position_info.id

        user_data = self.user_helper.create_user(register_data)
        user_data.pop('password')

        return user_data
