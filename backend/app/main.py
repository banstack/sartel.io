from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import os
import json
import uuid
from pathlib import Path

from app.models import CreateLobbyResponse, JoinLobbyRequest
from app.websocket import manager
from app.game import lobby as lobby_service
from app.storage.memory_store import store

load_dotenv()

app = FastAPI(title="Sartel.io API", version="1.0.0")

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the path to the frontend build directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent
FRONTEND_BUILD_DIR = BASE_DIR / "frontend" / "dist"


@app.get("/health")
async def health_check():
    """Health check endpoint for Railway and monitoring"""
    return {
        "status": "healthy",
        "service": "sartel.io-backend",
        "version": "1.0.0"
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Sartel.io API",
        "docs": "/docs",
        "health": "/health"
    }


@app.post("/api/lobby/create", response_model=CreateLobbyResponse)
async def create_lobby():
    """Create a new lobby"""
    lobby = lobby_service.create_lobby()
    return CreateLobbyResponse(
        lobby_id=lobby.lobby_id,
        message=f"Lobby created successfully. Share code: {lobby.lobby_id}"
    )


@app.get("/api/lobby/{lobby_id}")
async def get_lobby(lobby_id: str):
    """Get lobby information"""
    lobby_info = lobby_service.get_lobby_info(lobby_id)
    if not lobby_info:
        raise HTTPException(status_code=404, detail="Lobby not found or expired")
    return lobby_info


@app.get("/api/analytics")
async def get_analytics():
    """Get analytics data"""
    analytics = store.get_analytics()
    return analytics.model_dump()


@app.websocket("/ws/{lobby_id}/{player_id}")
async def websocket_endpoint(websocket: WebSocket, lobby_id: str, player_id: str):
    """WebSocket endpoint for real-time game communication"""
    await manager.connect(lobby_id, player_id, websocket)

    try:
        # Send connection confirmation
        await manager.send_personal_message(
            {
                "type": "connected",
                "player_id": player_id,
                "lobby_id": lobby_id
            },
            lobby_id,
            player_id
        )

        # Notify lobby about player count
        lobby = store.get_lobby(lobby_id)
        if lobby:
            await manager.broadcast_to_lobby(
                {
                    "type": "player_joined",
                    "player_count": len(lobby.players),
                    "players": lobby.players
                },
                lobby_id
            )

        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            message_type = message.get("type")

            # Handle different message types
            if message_type == "start_game":
                # Start the game
                game_state = lobby_service.start_game(lobby_id)
                if game_state:
                    await manager.broadcast_to_lobby(
                        {
                            "type": "game_started",
                            "letter": game_state.selected_letter,
                            "categories": game_state.categories,
                            "timer_duration": game_state.timer_duration,
                            "round_number": game_state.round_number
                        },
                        lobby_id
                    )
                else:
                    await manager.send_personal_message(
                        {
                            "type": "error",
                            "message": "Cannot start game. Need 2 players."
                        },
                        lobby_id,
                        player_id
                    )

            elif message_type == "submit_answer":
                # Submit an answer
                category = message.get("category")
                answer = message.get("answer")
                success = store.submit_answer(lobby_id, player_id, category, answer)
                if success:
                    await manager.send_personal_message(
                        {
                            "type": "answer_submitted",
                            "category": category,
                            "answer": answer
                        },
                        lobby_id,
                        player_id
                    )

            elif message_type == "submit_all_answers":
                # Player submitted all answers (timer expired or manual submit)
                answers = message.get("answers", {})
                for category, answer in answers.items():
                    store.submit_answer(lobby_id, player_id, category, answer)

                # Notify that player is ready
                await manager.broadcast_to_lobby(
                    {
                        "type": "player_ready",
                        "player_id": player_id
                    },
                    lobby_id
                )

                # Check if both players are ready
                game_state = store.get_game_state(lobby_id)
                lobby_obj = store.get_lobby(lobby_id)
                if game_state and lobby_obj:
                    all_submitted = all(
                        player in game_state.player_answers
                        for player in lobby_obj.players
                    )
                    if all_submitted:
                        # Reveal all answers
                        await manager.broadcast_to_lobby(
                            {
                                "type": "answers_revealed",
                                "player_answers": game_state.player_answers
                            },
                            lobby_id
                        )

            elif message_type == "ping":
                # Heartbeat/ping
                await manager.send_personal_message(
                    {"type": "pong"},
                    lobby_id,
                    player_id
                )

    except WebSocketDisconnect:
        manager.disconnect(lobby_id, player_id)
        # Notify remaining players
        await manager.broadcast_to_lobby(
            {
                "type": "player_disconnected",
                "player_id": player_id,
                "player_count": manager.get_lobby_player_count(lobby_id)
            },
            lobby_id
        )
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        manager.disconnect(lobby_id, player_id)


# Mount static files if the frontend build directory exists
if FRONTEND_BUILD_DIR.exists():
    # Mount static assets (JS, CSS, images, etc.)
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_BUILD_DIR / "assets")), name="assets")

    # Serve index.html for all other routes (SPA routing)
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve the frontend application for all non-API routes"""
        # Don't serve frontend for API routes or WebSocket routes
        if full_path.startswith("api/") or full_path.startswith("ws/") or full_path == "health":
            raise HTTPException(status_code=404, detail="Not found")

        index_file = FRONTEND_BUILD_DIR / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        else:
            raise HTTPException(status_code=404, detail="Frontend not built")
else:
    print("Warning: Frontend build directory not found. Only API endpoints will be available.")
