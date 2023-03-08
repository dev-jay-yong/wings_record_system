from peewee import MySQLDatabase, Model, IntegerField, DateField, CharField, BooleanField, ForeignKeyField, \
    DateTimeField, FloatField, TextField
import tomllib

with open("app/common/setting.toml", "rb") as f:
    setting_dict = tomllib.load(f)['DATABASE_SETTING']

db_name = setting_dict['dbname']
user = setting_dict['user']
password = setting_dict['password']
port = setting_dict['port']
host = setting_dict['host']

db = MySQLDatabase(db_name, user=user, password=password, host=host, port=port)

class BaseModel(Model):
    class Meta:
        database = db


class TeamModel(BaseModel):
    class Meta:
        db_table = 'teams'

    id = IntegerField(primary_key=True, db_column="id")
    name = CharField(max_length=50)
    team_logo = CharField(max_length=50)
    gender = BooleanField(default=False)
    created_at = DateField()


"""
create table teams
(
    id         int auto_increment
        primary key,
    name       varchar(50)          not null,
    created_at datetime             null,
    team_logo       varchar(50)          null,
    gender     tinyint(1) default 0 not null
);
"""


class TeamPerformanceModel(BaseModel):
    class Meta:
        db_table = 'team_performances'

    id = IntegerField(primary_key=True, db_column="id")
    competition_name = CharField(max_length=50)
    results = CharField(max_length=50)
    win_counts = IntegerField()
    lose_counts = IntegerField()
    start_date = DateField()
    end_date = DateField()
    team_id = IntegerField()


class TeamProfileModel(BaseModel):
    class Meta:
        db_table = 'team_profile'

    id = IntegerField(primary_key=True, db_column="id")
    team_id = IntegerField()
    hometown = CharField(max_length=255)
    affiliation = CharField(max_length=255)
    chairman = CharField(max_length=20)
    captain = CharField(max_length=20)


class TeamHistoryModel(BaseModel):
    class Meta:
        db_table = "team_history"

    id = IntegerField(primary_key=True, db_column="id")
    team_id = IntegerField()
    title = CharField(max_length=500)
    content = TextField()


"""
create table team_performances
(
    id               int auto_increment
        primary key,
    competition_name varchar(50) not null,
    results          varchar(50) not null,
    win_counts       int         not null,
    lose_counts      int         not null,
    start_date       date        not null,
    end_date         date        not null,
    team_id          int         not null
);
"""


class TeamUserModel(BaseModel):
    class Meta:
        db_table = 'team_users'

    id = IntegerField(primary_key=True, db_column="id")
    team_id = IntegerField()
    user_id = IntegerField()


"""
create table team_users
(
    id      int auto_increment
        primary key,
    team_id int not null,
    user_id int not null
);
"""


class PositionModel(BaseModel):
    class Meta:
        db_table = 'positions'

    id = IntegerField(primary_key=True, db_column="id")
    position_name = CharField(max_length=50, null=False)
    position_code = CharField(max_length=5, null=False)


"""
create table position
(
    id            int auto_increment
        primary key,
    position_name varchar(50) not null,
    position_code varchar(5)  not null
);
"""


class UserModel(BaseModel):
    class Meta:
        db_table = 'users'

    id = IntegerField(primary_key=True, db_column="id")
    identifier = CharField(max_length=50)
    password = CharField(max_length=255)
    name = CharField(max_length=50)
    birth = DateField()
    age = IntegerField()
    number = IntegerField()
    position = ForeignKeyField(PositionModel, to_field="id")
    token = CharField(max_length=255)
    profile_image = CharField(max_length=255)
    role = CharField(max_length=20)
    exit_flag = BooleanField(default=False)
    confirm = BooleanField(default=False)
    height = FloatField()
    weight = FloatField()


"""
create table users
(
    id            int auto_increment
        primary key,
    user_id       varchar(50)                  null,
    password      varchar(255)                 not null,
    name          varchar(50)                  null,
    birth         date                         not null,
    age           int                          null,
    number        int                          null,
    position      varchar(50)                  null,
    token         varchar(255)                 null,
    role          varchar(20) default 'player' not null,
    exit_flag     tinyint(1)  default 0        not null,
    register_date date                         null,
    confirm       tinyint(1)  default 0        null,
    profile_image varchar(255)                 null
);
"""


class PlayerRecordModel(BaseModel):

    class Meta:
        db_table = 'player_record'

    id = IntegerField()
    record_name = CharField(max_length=50)
    record_type = CharField(max_length=50)
    created_at = DateTimeField()
    user_id = IntegerField()
    team_id = IntegerField()


"""
create table player_record
(
    id          int auto_increment
        primary key,
    record_name varchar(50)                        not null,
    record_type varchar(50)                        not null,
    created_at  datetime default CURRENT_TIMESTAMP not null,
    user_id     int                                not null,
    team_id     int                                not null
);

create index player_record_team_id_index
    on player_record (team_id);

create index player_record_user_id_index
    on player_record (user_id);

create index player_record_user_id_team_id_index
    on player_record (user_id, team_id);
"""


class PlayerRecordModel(BaseModel):

    class Meta:
        db_table = 'player_record'

    id = IntegerField()
    record_name = CharField(max_length=50)
    record_type = CharField(max_length=50)
    created_at = DateTimeField()
    user_id = IntegerField()
    team_id = IntegerField()
    set_id = IntegerField()

class SetRecordModel(BaseModel):

    class Meta:
        db_table = 'set_record'

    id = IntegerField()
    set_name = CharField(max_length=255)
    match_id = IntegerField()
    team_id = IntegerField()
    match_date = DateField()
    result = BooleanField()
    set = IntegerField()
    my_team_score = IntegerField()
    other_team_score = IntegerField()


class MatchRecordModel(BaseModel):
    class Meta:
        db_table = 'match_record'

    id = IntegerField(primary_key=True, db_column="id")
    match_date = DateTimeField()
    team_id = IntegerField()
    other_team_name = CharField(max_length=50)
    other_team_id = IntegerField()
    win_set_score = IntegerField()
    lose_set_score = IntegerField()
    total_set_score = IntegerField()
    created_at = DateTimeField()


"""
create table match_record
(
    id              int auto_increment
        primary key,
    match_date      datetime                           not null,
    team_id         int                                not null,
    other_team_name varchar(50)                        null,
    other_team_id   int                                null,
    win_set_score   int      default 0                 null,
    lose_set_score  int      default 0                 null,
    total_set_score int                                not null,
    created_at      datetime default CURRENT_TIMESTAMP not null
);

"""


class PhotoModel(BaseModel):
    class Meta:
        db_table = 'photos'

    id = IntegerField(primary_key=True, db_column="id")
    user_id = IntegerField()
    image_url = CharField(max_length=255)
"""
create table photos
(
    id        int auto_increment
        primary key,
    user_id   int          not null,
    image_url varchar(255) not null
);
"""


class PrizeModel(BaseModel):
    class Meta:
        db_table = 'prizes'

    id = IntegerField(primary_key=True, db_column="id")
    prize_name = CharField(max_length=50)
    created_at = DateField()
    user_id = IntegerField()
    team_id = IntegerField()


"""
create table prizes
(
    id         int auto_increment
        primary key,
    prize_name varchar(50) not null,
    created_at date        null,
    user_id    int         null,
    team_id    int         null
);
"""


class TripleCrownModel(BaseModel):
    class Meta:
        db_table = 'triple_crowns'

    id = IntegerField(primary_key=True, db_column="id")
    user_id = IntegerField()
    back_attack_count = IntegerField()
    serve_count = IntegerField()
    block_count = IntegerField()
    created_at = DateField()
    match_id = IntegerField()
"""
create table triple_crowns
(
    id                int auto_increment
        primary key,
    user_id           int                                not null,
    back_attack_count int                                not null,
    serve_count       int                                not null,
    block_count       int                                not null,
    created_at        datetime default CURRENT_TIMESTAMP not null,
    match_id          int                                null
);
"""


class ReferenceRecordModel(BaseModel):
    class Meta:
        db_table = 'reference_records'

    id = IntegerField(primary_key=True, db_column="id")
    user_id = IntegerField()
    record_name = CharField(50)
    created_at = DateField()
"""
create table reference_records
(
    id          int auto_increment
        primary key,
    user_id     int                                not null,
    record_name varchar(50)                        not null,
    created_at  datetime default CURRENT_TIMESTAMP not null
);
"""



if __name__ == "__main__":
    print(UserModel.select().execute())
    print(MatchRecordModel.select().execute())
