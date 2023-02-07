from playhouse.shortcuts import model_to_dict

from models.team_models import TeamHelper, TeamHistoryModel
from models.user_model import UserHelper
from errors import exceptions as ex

import bcrypt


class Team:
    def __init__(self):
        self.team_helper = TeamHelper()
        self.user_helper = UserHelper()
        self.detail_record_structure = {
            "attack": {
                "attack": 0,
                "attack_success": 0,
                "attack_miss": 0,
                "blocking_shut_out": 0
            },
            "serve": {
                "serve_success": 0,
                "serve_miss": 0
            },
            "block": {
                "block_success": 0,
                "block": 0,
                "block_miss": 0,
                "block_fail": 0
            },
            "dig": {
                "dig": 0,
                "dig_success": 0,
                "dig_fail": 0,
            },
            "serve_receive": {
                "receive": 0,
                "receive_success": 0,
                "receive_miss": 0
            }
        }

    def get_teams(self, gender: bool) -> list[dict]:
        teams = [model_to_dict(x) for x in self.team_helper.get_teams_by_gender_code(gender)]

        return teams

    def get_team_coach_info(self, team_id) -> dict:
        coach_data = self.team_helper.get_coach_info_by_team_id(team_id)

        if coach_data is None:
            raise ex.NotExistCoachException

        profile_image = self.team_helper.get_one_team_users_by_team_id(coach_data.id, team_id).profile_image

        coach_position = model_to_dict(coach_data.position)
        coach_data = coach_data.__dict__['__data__']
        coach_data.update(coach_position)
        coach_data.pop('position')
        coach_data.pop('id')
        coach_data['profile_image'] = profile_image

        return coach_data

    def get_team_introduction(self, team_id) -> dict:
        team_info = self.team_helper.get_one_team_by_id(team_id, is_dict=True)
        team_performance = [model_to_dict(x) for x in self.team_helper.get_team_performances_by_team_id(team_id)]
        team_info['performance'] = team_performance

        coach_data = self.team_helper.get_coach_info_by_team_id(team_id)
        team_info['price'] = {'seoul_league': 0, 'national_convention': 0}
        team_info['info'] = self.team_helper.get_team_profile(team_id)
        team_info['coach'] = coach_data.name if coach_data else "공석"

        return team_info

    def get_team_players(self, team_id) -> list[dict]:

        result = [{
                "id": player.id,
                "name": player.name,
                "number": player.number,
                "profile_image": player.profile_image,
                "position_name": player.position.position_name,
                "position_code": player.position.position_code,
            } for player in self.team_helper.get_team_players_by_team_id(team_id)]

        return result

    def team_player_info(self, player_id, team_id):
        detail_record = self.detail_record_structure
        user_info = self.team_helper.get_one_team_users_by_team_id(player_id, team_id)

        if user_info:
            user_info = user_info.__dict__['__data__']

        player_record = {'score_rank': TeamHelper().get_active_name_rank_by_user_id(player_id,
                                                                                    ["attack_success", "block_success",
                                                                                     "serve_success"]),
                         'attack_rank': TeamHelper().get_active_name_rank_by_user_id(player_id, "attack_success"),
                         'serve_rank': TeamHelper().get_active_name_rank_by_user_id(player_id, "serve_success"),
                         'block_rank': TeamHelper().get_active_name_rank_by_user_id(player_id, "block_success"),
                         'receive_rank': TeamHelper().get_active_name_rank_by_user_id(player_id, "receive_success")}

        for record_type, record_data in detail_record.items():
            for x in self.team_helper.get_player_record(player_id, team_id, record_type):
                record_data[x.record_name] = x.count

        for x in self.team_helper.get_match_record(team_id):
            detail_record.update({"set_count": x.set_count, "match_count": x.match_count})

        detail_record['attack']['accuracy'] = round(
            detail_record['attack']['attack_success'] / detail_record['attack']['attack'], 2) * 100 if \
        detail_record['attack']['attack'] else 0

        detail_record['serve_receive'] = self.get_record_possession(detail_record['serve_receive'], 'receive_success', team_id)
        detail_record['attack'] = self.get_record_possession(detail_record['attack'], 'attack_success', team_id)
        detail_record['block'] = self.get_record_possession(detail_record['block'], 'block_success', team_id)
        detail_record['serve'] = self.get_record_possession(detail_record['serve'], 'serve_success', team_id)
        detail_record['dig'] = self.get_record_possession(detail_record['dig'], 'dig_success', team_id)

        photo_gallery = [x.__dict__['__data__'] for x in self.user_helper.get_photo_gallery(player_id)]
        reference_record = [x.__dict__['__data__'] for x in self.user_helper.get_reference_record_by_user_id(player_id)]
        triple_crown = [x.__dict__['__data__'] for x in self.user_helper.get_triple_crown_by_user_id(player_id)]
        prize = [x.__dict__['__data__'] for x in self.user_helper.get_prize_by_user_id(player_id)]

        data = {"prize": prize, "triple_crown": triple_crown, "reference_record": reference_record}

        return {"user": user_info, "detail_record": detail_record, "player_record": player_record,
                "photo_gallery_urls": photo_gallery, "job": data}

    def get_record_possession(self, data, record_name, team_id):
        team_record_count = self.team_helper.get_team_record_count(team_id, record_name)
        data['possession'] = 0 if team_record_count == 0 else round(data[record_name] / team_record_count, 2) * 100
        return data

    def get_team_record(self, team_id, record_type):
        result = self.detail_record_structure

        for x in self.team_helper.get_team_record_by_team_id_and_record_type(team_id, record_type):
            result[record_type][x.record_name] = x.count

        for x in self.team_helper.get_match_record(team_id):
            result[record_type].update({"set_count": x.set_count, "match_count": x.match_count})

        return result[record_type]
