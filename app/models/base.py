from peewee import MySQLDatabase, Model
from playhouse.reflection import generate_models
import logging
import tomllib


with open("app/common/setting.toml", "rb") as f:
    setting_dict = tomllib.load(f)['DATABASE_SETTING']

logger = logging.getLogger("peewee")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

db_name = setting_dict['dbname']
user = setting_dict['user']
password = setting_dict['password']
port = setting_dict['port']
host = setting_dict['host']

db = MySQLDatabase(db_name, user=user, password=password, host=host, port=port)

class BaseModel(Model):

    class Meta:
        database = db
