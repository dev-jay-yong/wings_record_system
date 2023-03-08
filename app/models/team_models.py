from playhouse.shortcuts import model_to_dict
from models.base import TeamModel, TeamPerformanceModel, TeamUserModel, UserModel, PositionModel, \
    PlayerRecordModel, MatchRecordModel, db, TeamProfileModel, TeamHistoryModel, SetRecordModel
from peewee import fn, Select

import functools


class TeamHelper:
    def __init__(self):
        self.table = TeamModel
        self.team_performance_table = TeamPerformanceModel
        self.team_user_table = TeamUserModel
        self.user_table = UserModel
        self.position_table = PositionModel
        self.player_record_table = PlayerRecordModel
        self.match_record_table = MatchRecordModel
        self.team_profile_table = TeamProfileModel
        self.team_history_table = TeamHistoryModel
        self.set_record_table = SetRecordModel

    def __exit__(self, exc_type, exc_value, traceback):

        if not db.is_closed():
            db.close()

    def wrapper(func):
        @functools.wraps(func)
        def wrap(self, *args, **kwargs):
            with db.connection_context():
                return func(self, *args, **kwargs)

        return wrap

    @wrapper
    def get_teams_by_gender_code(self, gender_code: bool):
        return self.table.select().where(self.table.gender == gender_code).execute()

    @wrapper
    def get_team_history_by_team_id(self, team_id: int, select_query: tuple = None):
        condition = self.team_history_table.team_id == team_id
        return self.team_history_table.select(*select_query).where(condition).execute()

    @wrapper
    def get_one_history_by_id(self, history_id: int):
        return self.team_history_table.get_or_none(self.team_history_table.id == history_id)

    @wrapper
    def get_one_team_by_id(self, user_id, is_dict=False):
        result = self.table.get_or_none(self.table.id == user_id)

        if result is None:
            return result

        return model_to_dict(result) if is_dict else result

    @wrapper
    def get_team_win_lose_score(self, team_id):
        select_query = (
            fn.SUM(self.team_performance_table.win_counts).alias('total_win_count'),
            fn.SUM(self.team_performance_table.lose_counts).alias('total_lose_count')
        )
        result = self.team_performance_table.select(*select_query).where(
            self.team_performance_table.team_id == team_id).execute()

        return result

    @wrapper
    def get_team_performances_by_team_id(self, team_id):
        result = self.team_performance_table.select().where(self.team_performance_table.team_id == team_id).execute()

        return result

    @wrapper
    def get_one_team_users_by_team_id(self, user_id, team_id, role=None):
        join_on_query = self.user_table.id == self.team_user_table.user_id
        select_query = (
            self.user_table.id,
            self.user_table.name,
            self.user_table.number,
            self.user_table.profile_image,
            self.user_table.weight,
            self.user_table.height,
            self.user_table.birth,
            self.position_table.position_name.alias('position_name'),
            self.position_table.position_code.alias('position_code'),
        )

        condition = (self.team_user_table.team_id == team_id) & \
                    (self.user_table.exit_flag == 0) & \
                    (self.user_table.confirm == 1) & \
                    (self.user_table.id == user_id)

        if role:
            condition &= (self.user_table.role == role)

        return self.user_table.select(*select_query).join(self.position_table).join(self.team_user_table,
                                                                                    on=join_on_query).where(
            (condition)).limit(1).first()

    @wrapper
    def get_team_players_by_team_id(self, team_id):
        join_on_query = self.user_table.id == self.team_user_table.user_id

        select_query = (
            self.user_table.id,
            self.user_table.name,
            self.user_table.number,
            self.user_table.profile_image,
            self.position_table.position_name.alias('position_name'),
            self.position_table.position_code.alias('position_code'),
        )

        condition = (
                (self.team_user_table.team_id == team_id) &
                (self.user_table.exit_flag == 0) &
                (self.user_table.role == 'player') &
                (self.user_table.confirm == 1)
        )

        return self.user_table.select(*select_query).join(self.position_table).join(self.team_user_table,
                                                                                    on=join_on_query).where(
            condition).execute()

    @wrapper
    def get_team_profile(self, team_id):
        select_query = (
            self.team_profile_table.affiliation,
            self.team_profile_table.hometown,
            self.team_profile_table.chairman,
            self.team_profile_table.captain
        )

        result = self.team_profile_table.select(*select_query).where(self.team_profile_table.team_id == team_id).limit(
            1).first()
        return result.__dict__['__data__'] if result else None

    @wrapper
    def get_team_record_by_team_id_and_record_type(self, team_id, record_type=None):
        condition = (self.player_record_table.team_id == team_id)
        select_query = (
            self.player_record_table.record_name,
            fn.Count(self.player_record_table.record_name).alias('count')
        )

        if record_type:
            condition &= (self.player_record_table.record_type == record_type)

        return self.player_record_table.select(*select_query) \
            .where(condition).group_by(self.player_record_table.record_name)

    @wrapper
    def get_player_record(self, player_id, team_id, record_type=None):
        condition = (self.player_record_table.team_id == team_id) & (self.player_record_table.user_id == player_id)
        select_query = (
            self.player_record_table.record_name,
            fn.Count(self.player_record_table.record_name).alias('count')
        )

        if record_type:
            condition &= (self.player_record_table.record_type == record_type)

        return self.player_record_table.select(*select_query) \
            .where(condition).group_by(self.player_record_table.record_name)

    @wrapper
    def get_team_record_count(self, team_id, record_name):
        select_query = fn.COUNT(self.player_record_table.team_id).alias('count')
        condition = (self.player_record_table.team_id == team_id) & (
                self.player_record_table.record_name == record_name)

        return self.player_record_table.select(select_query).where(condition).get().count

    @wrapper
    def get_match_record(self, team_id):
        condition = (self.match_record_table.team_id == team_id)
        select_query = (
            fn.COUNT(self.match_record_table.id).alias('match_count'),
            fn.SUM(self.match_record_table.total_set_score).alias('set_count')
        )

        return self.match_record_table.select(*select_query).where(condition).group_by(
            self.match_record_table.team_id).execute()

    @wrapper
    def get_coach_info_by_team_id(self, team_id):
        select_query = (
            self.user_table.id,
            self.user_table.name,
            self.user_table.birth,
            self.user_table.role,
            self.position_table.position_name,
            self.position_table.position_code,
        )

        join_on_query = self.user_table.id == self.team_user_table.user_id
        conditions = (
                (self.user_table.role == 'coach') &
                (self.team_user_table.team_id == team_id) &
                (self.user_table.exit_flag == False)
        )

        result = self.user_table.select(*select_query). \
            join(self.position_table). \
            join(self.team_user_table, on=join_on_query). \
            where(conditions).limit(1)

        result = result.get() if result else None

        return result

    @wrapper
    def get_set_record_data_by_user_id(self, user_id, record_name_list=None):

        select_query = (
            self.player_record_table.record_name,
            fn.COUNT(self.player_record_table.record_name).alias('count'),
            self.set_record_table.set_name.alias('set_name'),
        )
        join_on_query = (self.set_record_table.id == self.player_record_table.set_id)
        condition = self.player_record_table.user_id == user_id

        if record_name_list is not None:
            condition &= self.player_record_table.record_name.in_(record_name_list)

        group_by_query = (self.player_record_table.set_id, self.player_record_table.record_name)

        result = self.player_record_table.select(*select_query).join(self.set_record_table, on=join_on_query).where(condition).group_by(*group_by_query)

        return result

    @wrapper
    def get_active_name_rank_by_user_id(self, user_id, active_name="attack_success"):
        rank = fn.rank().over(order_by=[fn.COUNT(self.player_record_table.id).desc()])

        if type(active_name) == str:
            condition = self.player_record_table.record_name == active_name
        else:
            condition = self.player_record_table.record_name.in_(active_name)

        subq = (self.player_record_table
                .select(self.player_record_table.user_id,
                        fn.COUNT(self.player_record_table.user_id).alias('total_count'),
                        rank.alias('rank')).where(condition)
                .group_by(self.player_record_table.user_id))

        query = (Select(columns=[subq.c.total_count, subq.c.rank])
                 .from_(subq).where(subq.c.user_id == user_id)
                 .bind(db))

        return query[0] if query else {"total_count": 0, "rank": 0}


if __name__ == '__main__':
    print(TeamHelper().get_team_win_lose_score(1))
