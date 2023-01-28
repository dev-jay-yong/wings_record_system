from . import BaseResponse


class TeamResponse(BaseResponse):
    data: list = [
        {
            "id": 1,
            "name": "team_name",
            "team_logo": "logo url",
            "gender": True,
            "created_at": "2023-01-23"
        }
    ]


class TeamIntroductionResponse(BaseResponse):
    data: dict = {
        "id": 1,
        "name": "팀명",
        "team_logo": "로고 url",
        "gender": True,
        "created_at": "2023-01-23",
        "performance": [
            {
                "id": 1,
                "competition_name": "2022 대한체육회장기 전국생활체육배구대회 (단양)",
                "results": "4강 진출",
                "win_counts": 6,
                "lose_counts": 2,
                "start_date": "2022-12-03",
                "end_date": "2022-12-04",
                "team_id": 1
            }
        ],
        "coach": {
            "name": "이태봉",
            "birth": "1998-02-05",
            "role": "coach",
            "position_name": "아웃사이드 히터",
            "position_code": "OH"
        }
    }


class TeamPlayersResponse(BaseResponse):
    data: list = [
        {
            "id": 1,
            "name": "홍길동",
            "profile_image": "프로필 이미지 url",
            "position_name": "아웃사이드 히터",
            "position_code": "OH"
        },
        {
            "id": 2,
            "name": "사또",
            "profile_image": "프로필 이미지 url",
            "position_name": "아포짓 스파이커",
            "position_code": "OP"
        },
        {
            "id": 3,
            "name": "뭐하지",
            "profile_image": "프로필 이미지 url",
            "position_name": "미들블로커",
            "position_code": "MB"
        },
    ]


class TeamRecordResponse(BaseResponse):
    data: dict = {
        "data": {
        "match_count": 1,
        "set_count": 1,
        "attack": 2,
        "attack_success": 1,
        "attack_miss": 1,
        "blocking_shut_out": 0
        }
    }
