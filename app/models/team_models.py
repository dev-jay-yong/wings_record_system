from playhouse.shortcuts import model_to_dict
from app.models.base import TeamModel, TeamPerformanceModel, TeamUserModel, UserModel, PositionModel, \
    PlayerRecordModel, MatchRecordModel, db
from peewee import fn, Select


class TeamHelper:
    def __init__(self):
        self.table = TeamModel
        self.team_performance_table = TeamPerformanceModel
        self.team_user_table = TeamUserModel
        self.user_table = UserModel
        self.position_table = PositionModel
        self.player_record_table = PlayerRecordModel
        self.match_record_table = MatchRecordModel

    def get_teams_by_gender_code(self, gender_code: bool):
        return self.table.select().where(self.table.gender == gender_code).execute()

    def get_one_team_by_id(self, user_id, is_dict=False):
        result = self.table.get_or_none(self.table.id == user_id)
        return model_to_dict(result) if is_dict else result

    def get_team_performances_by_team_id(self, team_id):
        result = self.team_performance_table.select().where(self.team_performance_table.team_id == team_id).execute()

        return result

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

    def get_team_record_count(self, team_id, record_name):
        select_query = fn.COUNT(self.player_record_table.team_id).alias('count')
        condition = (self.player_record_table.team_id == team_id) & (self.player_record_table.record_name == record_name)

        return self.player_record_table.select(select_query).where(condition).get().count

    def get_match_record(self, team_id):
        condition = (self.match_record_table.team_id == team_id)
        select_query = (
            fn.COUNT(self.match_record_table.id).alias('match_count'),
            fn.SUM(self.match_record_table.total_set_score).alias('set_count')
        )

        return self.match_record_table.select(*select_query).where(condition).group_by(self.match_record_table.team_id).execute()

    def get_coach_info_by_team_id(self, team_id):
        select_query = (
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

        result = self.user_table.select(*select_query).\
                        join(self.position_table).\
                        join(self.team_user_table, on=join_on_query).\
                        where(conditions).limit(1)

        result = result.get() if result else None

        return result

    def get_active_name_rank_by_user_id(self, user_id, active_name="attack_success"):
        rank = fn.rank().over(order_by=[fn.COUNT(self.player_record_table.id).desc()])

        if type(active_name) == str:
            condition = self.player_record_table.record_name == active_name
        else:
            condition = self.player_record_table.record_name.in_(active_name)

        subq = (self.player_record_table
                .select(self.player_record_table.user_id, fn.COUNT(self.player_record_table.user_id).alias('total_count'),
                        rank.alias('rank')).where(condition)
                .group_by(self.player_record_table.user_id))

        query = (Select(columns=[subq.c.total_count, subq.c.rank])
                 .from_(subq).where(subq.c.user_id == user_id)
                 .bind(db))

        return query[0] if query else {"total_count": 0, "rank": 0}


if __name__ == '__main__':
    print(TeamHelper().get_team_record_count(1, 'attack_success'))
