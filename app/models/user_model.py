from playhouse.shortcuts import model_to_dict

from app.models.base import BaseModel
from peewee import *


class UserModel(BaseModel):
    class Meta:
        db_table = 'users'

    id = IntegerField(primary_key=True, db_column="id")
    user_id = CharField(max_length=50)
    password = CharField(max_length=255)
    name = CharField(max_length=50)
    birth = DateField()
    age = IntegerField()
    number = IntegerField()
    position = CharField(max_length=50)
    token = CharField(max_length=255)
    confirm = BooleanField(default=False)

"""
-- auto-generated definition
create table users
(
    id       int auto_increment
        primary key,
    user_id  varchar(50)          null,
    password varchar(255)         not null,
    name     varchar(50)          null,
    birth    date                 not null,
    age      int                  null,
    number   int                  null,
    position varchar(50)          null,
    token    varchar(255)         null,
    confirm  tinyint(1) default 0 null
);

"""

class UserHelper:
    def __init__(self):
        self.table = UserModel

    def create_user(self, data):
        return model_to_dict(self.table.create(**data))

    def get_one_user_by_id(self, user_id, is_dict=False):
        result = self.table.get_or_none(self.table.user_id == user_id)
        return model_to_dict(result) if is_dict else result


if __name__ == '__main__':
    print([model_to_dict(x) for x in UserModel.select().execute()])
