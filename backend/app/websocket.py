from fastapi import WebSocket
from typing import Dict, List
import json


class ConnectionManager:
    """Manages WebSocket connections grouped by lobby"""

    def __init__(self):
        # Structure: {lobby_id: {player_id: WebSocket}}
        self.active_connections: Dict[str, Dict[str, WebSocket]] = {}

    async def connect(self, lobby_id: str, player_id: str, websocket: WebSocket):
        """Accept WebSocket connection and add to lobby"""
        await websocket.accept()
        if lobby_id not in self.active_connections:
            self.active_connections[lobby_id] = {}
        self.active_connections[lobby_id][player_id] = websocket

    def disconnect(self, lobby_id: str, player_id: str):
        """Remove WebSocket connection from lobby"""
        if lobby_id in self.active_connections:
            if player_id in self.active_connections[lobby_id]:
                del self.active_connections[lobby_id][player_id]
            # Clean up empty lobbies
            if not self.active_connections[lobby_id]:
                del self.active_connections[lobby_id]

    async def send_personal_message(self, message: dict, lobby_id: str, player_id: str):
        """Send message to a specific player"""
        if lobby_id in self.active_connections:
            if player_id in self.active_connections[lobby_id]:
                websocket = self.active_connections[lobby_id][player_id]
                await websocket.send_text(json.dumps(message))

    async def broadcast_to_lobby(self, message: dict, lobby_id: str):
        """Broadcast message to all players in a lobby"""
        if lobby_id in self.active_connections:
            disconnected = []
            for player_id, websocket in self.active_connections[lobby_id].items():
                try:
                    await websocket.send_text(json.dumps(message))
                except Exception:
                    disconnected.append(player_id)

            # Clean up disconnected players
            for player_id in disconnected:
                self.disconnect(lobby_id, player_id)

    def get_lobby_player_count(self, lobby_id: str) -> int:
        """Get number of connected players in a lobby"""
        if lobby_id in self.active_connections:
            return len(self.active_connections[lobby_id])
        return 0

    def is_player_connected(self, lobby_id: str, player_id: str) -> bool:
        """Check if a player is connected to a lobby"""
        if lobby_id in self.active_connections:
            return player_id in self.active_connections[lobby_id]
        return False


# Global connection manager instance
manager = ConnectionManager()
