from typing import Optional, Dict
from datetime import datetime, timedelta
from backend.app.models import Lobby, GameState, Analytics, LobbyState


class MemoryStore:
    """In-memory storage for lobbies, game state, and analytics"""

    def __init__(self):
        self.lobbies: Dict[str, Lobby] = {}
        self.game_states: Dict[str, GameState] = {}
        self.analytics = Analytics()

    # Lobby operations
    def create_lobby(self, lobby_id: str, expiration_minutes: int = 30) -> Lobby:
        """Create a new lobby"""
        now = datetime.utcnow()
        lobby = Lobby(
            lobby_id=lobby_id,
            players=[],
            state=LobbyState.WAITING,
            created_at=now,
            expires_at=now + timedelta(minutes=expiration_minutes)
        )
        self.lobbies[lobby_id] = lobby
        self.analytics.total_lobbies_created += 1
        return lobby

    def get_lobby(self, lobby_id: str) -> Optional[Lobby]:
        """Get lobby by ID"""
        lobby = self.lobbies.get(lobby_id)
        if lobby and datetime.utcnow() > lobby.expires_at:
            # Lobby expired, remove it
            self.delete_lobby(lobby_id)
            return None
        return lobby

    def update_lobby(self, lobby_id: str, lobby: Lobby) -> None:
        """Update lobby"""
        self.lobbies[lobby_id] = lobby

    def delete_lobby(self, lobby_id: str) -> None:
        """Delete lobby and associated game state"""
        if lobby_id in self.lobbies:
            del self.lobbies[lobby_id]
        if lobby_id in self.game_states:
            del self.game_states[lobby_id]

    def add_player_to_lobby(self, lobby_id: str, player_id: str) -> bool:
        """Add player to lobby, returns True if successful"""
        lobby = self.get_lobby(lobby_id)
        if not lobby:
            return False
        if len(lobby.players) >= 2:
            return False
        if player_id not in lobby.players:
            lobby.players.append(player_id)
            self.update_lobby(lobby_id, lobby)
            self.analytics.total_players += 1
        return True

    # Game state operations
    def create_game_state(self, lobby_id: str) -> GameState:
        """Create a new game state for a lobby"""
        game_state = GameState(lobby_id=lobby_id)
        self.game_states[lobby_id] = game_state
        return game_state

    def get_game_state(self, lobby_id: str) -> Optional[GameState]:
        """Get game state by lobby ID"""
        return self.game_states.get(lobby_id)

    def update_game_state(self, lobby_id: str, game_state: GameState) -> None:
        """Update game state"""
        self.game_states[lobby_id] = game_state

    def submit_answer(self, lobby_id: str, player_id: str, category: str, answer: str) -> bool:
        """Submit an answer for a player"""
        game_state = self.get_game_state(lobby_id)
        if not game_state:
            return False

        if player_id not in game_state.player_answers:
            game_state.player_answers[player_id] = {}

        game_state.player_answers[player_id][category] = answer
        self.update_game_state(lobby_id, game_state)
        self.analytics.total_words_created += 1
        return True

    # Analytics operations
    def get_analytics(self) -> Analytics:
        """Get current analytics"""
        return self.analytics

    def cleanup_expired_lobbies(self) -> int:
        """Clean up expired lobbies, returns count of removed lobbies"""
        now = datetime.utcnow()
        expired = [
            lobby_id for lobby_id, lobby in self.lobbies.items()
            if now > lobby.expires_at
        ]
        for lobby_id in expired:
            self.delete_lobby(lobby_id)
        return len(expired)


# Global store instance
store = MemoryStore()
