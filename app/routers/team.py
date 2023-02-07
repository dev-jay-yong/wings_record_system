from enum import Enum

from fastapi import APIRouter

from routers.response_model.team_response import *
from services.team_service import Team

router = APIRouter(prefix="/team", tags=["team"])


@router.get(
    path="",
    response_model=TeamResponse,
)
async def get_teams(gender: bool = True) -> dict:
    """
    ### 팀 리스트 조회 <br><br>
    ```gender```: 조회할 팀 (bool) - query param | default: true | true -> 남성, false -> 여성
    """

    result = Team().get_teams(gender)
    return {"data": result}

@router.get(
    path="/introduction",
    response_model=TeamIntroductionResponse
)
async def get_team_introduction(team_id: int) -> dict:
    """
    ### 팀 소개 <br><br>
    ```team_id```: 팀 아이디 (int) - query param
    """
    result = Team().get_team_introduction(team_id)
    return {"data": result}


@router.get(
    path="/coach"
)
async def get_team_coach(team_id: int) -> dict:
    """
    ### 팀 코치 정보 조회 <br><br>
    ```team_id```: 팀 아이디 (int) - query param
    """
    result = Team().get_team_coach_info(team_id)
    return {"data": result}


@router.get(
    path="/players",
    response_model=TeamPlayersResponse
)
async def get_team_player_list(team_id: int) -> dict:
    """
    ### 팀 소개 <br><br>
    ```team_id```: 팀 아이디 (int) - query param
    """
    result = Team().get_team_players(team_id)
    return {"data": result}


class RecordType(str, Enum):
    serve = "serve"
    block = "block"
    attack = "attack"
    serve_receive = "serve_receive"
    dig = "dig"


@router.get(
    path="/record/{record_type}",
    response_model=TeamRecordResponse
)
async def get_team_record(team_id: int, record_type: RecordType) -> dict:
    """
    ### 팀 소개 <br><br>
    ```team_id```: 팀 아이디 (int) - query param
    """

    result = Team().get_team_record(team_id, record_type.name)
    return {"data": result}


@router.get(
    path="/player/{player_id}"
)
async def get_player_info(player_id: int, team_id: int) -> dict:
    result = Team().team_player_info(player_id, team_id)

    return {"data": result}

@router.get(
    path="/history/{team_id}"
)
async def get_team_history(team_id: int, content_id: int = None) -> dict:
    result = Team().team_history(team_id, content_id)

    return {"data": result}
