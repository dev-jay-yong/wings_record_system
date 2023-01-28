from playhouse.shortcuts import model_to_dict
from app.models.base import UserModel, PhotoModel, ReferenceRecordModel, TripleCrownModel, PrizeModel, PositionModel


class UserHelper:
    def __init__(self):
        self.table = UserModel
        self.user_photo_table = PhotoModel
        self.reference_record_table = ReferenceRecordModel
        self.triple_crown_table = TripleCrownModel
        self.position_table = PositionModel
        self.prize_table = PrizeModel

    def create_user(self, data):
        return model_to_dict(self.table.create(**data))

    def get_position_by_name(self, position_name):
        return self.position_table.get_or_none(self.position_table.position_name == position_name)

    def get_one_user_by_id(self, user_id, is_dict=False):
        result = self.table.get_or_none(self.table.identifier == user_id)
        return model_to_dict(result) if is_dict else result

    def get_user_by_token(self, token: str) -> UserModel:
        return self.table.get_or_none(self.table.token == token)

    def get_photo_gallery(self, user_id):
        return self.user_photo_table.select().where(self.user_photo_table.user_id == user_id).execute()

    def get_reference_record_by_user_id(self, user_id):
        return self.reference_record_table.select().where(self.reference_record_table.user_id == user_id).execute()

    def get_triple_crown_by_user_id(self, user_id):
        return self.triple_crown_table.select().where(self.triple_crown_table.user_id == user_id).execute()

    def get_prize_by_user_id(self, user_id):
        return self.prize_table.select().where(self.prize_table.user_id == user_id).execute()



if __name__ == '__main__':
    print([x.image_url for x in UserHelper().get_photo_gallery(7)])

