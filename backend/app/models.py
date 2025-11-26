from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum


class LobbyState(str, Enum):
    WAITING = "waiting"
    PLAYING = "playing"
    REVIEWING = "reviewing"
    COMPLETED = "completed"


class Lobby(BaseModel):
    lobby_id: str
    players: List[str] = []
    state: LobbyState = LobbyState.WAITING
    created_at: datetime
    expires_at: datetime


class GameState(BaseModel):
    lobby_id: str
    round_number: int = 1
    selected_letter: Optional[str] = None
    categories: List[str] = [
        "Surnames",
        "Companies",
        "Countries",
        "Cities",
        "Animals",
        "Plants",
        "Items",
        "Food"
    ]
    player_answers: Dict[str, Dict[str, str]] = {}
    timer_started_at: Optional[datetime] = None
    timer_duration: int = 60  # seconds


class CreateLobbyResponse(BaseModel):
    lobby_id: str
    message: str


class JoinLobbyRequest(BaseModel):
    lobby_id: str
    player_id: str


class SubmitAnswerRequest(BaseModel):
    lobby_id: str
    player_id: str
    category: str
    answer: str


class SelfJudgeRequest(BaseModel):
    lobby_id: str
    player_id: str
    category: str
    valid: bool


class Analytics(BaseModel):
    total_lobbies_created: int = 0
    total_players: int = 0
    total_words_created: int = 0
    daily_stats: Dict[str, int] = {}
