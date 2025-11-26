import random
import string
from datetime import datetime
from typing import Optional
from app.models import Lobby, GameState, LobbyState
from app.storage.memory_store import store


def generate_lobby_id(length: int = 5) -> str:
    """Generate a random lobby ID"""
    # Use uppercase letters and digits for clarity
    chars = string.ascii_uppercase + string.digits
    # Keep trying until we get a unique ID
    while True:
        lobby_id = ''.join(random.choices(chars, k=length))
        if not store.get_lobby(lobby_id):
            return lobby_id


def create_lobby() -> Lobby:
    """Create a new lobby"""
    lobby_id = generate_lobby_id()
    lobby = store.create_lobby(lobby_id)
    # Also create associated game state
    store.create_game_state(lobby_id)
    return lobby


def join_lobby(lobby_id: str, player_id: str) -> Optional[Lobby]:
    """Join an existing lobby"""
    lobby = store.get_lobby(lobby_id)
    if not lobby:
        return None

    if lobby.state != LobbyState.WAITING:
        return None

    success = store.add_player_to_lobby(lobby_id, player_id)
    if not success:
        return None

    return store.get_lobby(lobby_id)


def start_game(lobby_id: str) -> Optional[GameState]:
    """Start the game for a lobby"""
    lobby = store.get_lobby(lobby_id)
    if not lobby or len(lobby.players) != 2:
        return None

    # Update lobby state
    lobby.state = LobbyState.PLAYING
    store.update_lobby(lobby_id, lobby)

    # Get game state and select random letter
    game_state = store.get_game_state(lobby_id)
    if not game_state:
        return None

    # Select random letter from A-Z
    game_state.selected_letter = random.choice(string.ascii_uppercase)
    game_state.timer_started_at = datetime.utcnow()

    # Initialize player answers
    for player_id in lobby.players:
        game_state.player_answers[player_id] = {}

    store.update_game_state(lobby_id, game_state)
    return game_state


def get_lobby_info(lobby_id: str) -> Optional[dict]:
    """Get lobby and game state info"""
    lobby = store.get_lobby(lobby_id)
    if not lobby:
        return None

    game_state = store.get_game_state(lobby_id)

    return {
        "lobby": lobby.model_dump(),
        "game_state": game_state.model_dump() if game_state else None
    }
