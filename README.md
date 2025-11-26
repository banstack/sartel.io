# Sartel.io

A real-time multiplayer word game where two players compete to come up with words starting with a random letter for various categories.

## Project Status

✅ **Phase 1 Complete**: Core Infrastructure (MVP)
- Backend with FastAPI + WebSocket
- In-memory storage for lobbies and game state
- Frontend with React + Vite + Shadcn UI
- Basic lobby creation and joining
- WebSocket connection established

## Tech Stack

### Backend
- **Framework**: FastAPI
- **WebSockets**: Native FastAPI WebSocket support
- **Storage**: In-memory (Phase 1), Redis (Phase 3)
- **Language**: Python 3.11+

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite 6
- **UI Library**: Shadcn UI (Tailwind CSS v4)
- **Language**: TypeScript

### Deployment
- **Platform**: Railway
- **Architecture**: Monorepo (separate backend/frontend services)

## Project Structure

```
sartel.io/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── websocket.py         # WebSocket connection manager
│   │   ├── models.py            # Pydantic models
│   │   ├── game/
│   │   │   └── lobby.py         # Lobby management
│   │   └── storage/
│   │       └── memory_store.py  # In-memory storage
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Home.tsx         # Home page
│   │   │   ├── Lobby.tsx        # Lobby view
│   │   │   └── ui/              # Shadcn UI components
│   │   ├── hooks/
│   │   │   └── useWebSocket.ts  # WebSocket connection hook
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── .env.example
├── CLAUDE.md                    # Project requirements
├── RESEARCH.md                  # Architecture research
└── README.md
```

## Local Development

### Backend

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the development server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

4. Open browser to `http://localhost:5173`

## How to Play

1. **Create a Lobby**: Click "Create New Lobby" to generate a unique 5-character code
2. **Share Code**: Share the lobby code with a friend
3. **Join Lobby**: Friend enters the code to join
4. **Start Game**: Once both players are connected, either can start the game
5. **Play**: Fill in words for each category that start with the selected letter
6. **Review**: When time's up, review each other's answers and self-judge

## Game Rules

- Two players per lobby
- Random letter selected at game start
- 8 categories to fill (Surnames, Companies, Countries, Cities, Animals, Plants, Items, Food)
- 60-second timer shared between both players
- Players self-judge their answers
- Most valid words wins!

## Implementation Phases

### ✅ Phase 1: Core Infrastructure (Complete)
- [x] Backend setup with FastAPI + WebSocket
- [x] In-memory storage for lobbies/game state
- [x] Frontend setup with React + Vite + Shadcn
- [x] Basic lobby creation and joining
- [x] WebSocket connection establishment

### 🚧 Phase 2: Game Mechanics (Next)
- [ ] Random letter selection
- [ ] Category table rendering
- [ ] Shared timer implementation
- [ ] Answer submission flow
- [ ] Answer reveal and self-judging

### 📋 Phase 3: Production Ready
- [ ] Redis integration for storage
- [ ] Analytics tracking
- [ ] Railway deployment configuration
- [ ] CI/CD pipeline
- [ ] Error handling and edge cases

### 🎨 Phase 4: Polish
- [ ] Responsive design
- [ ] Loading states
- [ ] Disconnect handling
- [ ] Lobby expiration cleanup
- [ ] Basic unit tests

## API Endpoints

### REST Endpoints
- `GET /health` - Health check
- `GET /` - API info
- `POST /api/lobby/create` - Create new lobby
- `GET /api/lobby/{lobby_id}` - Get lobby info
- `GET /api/analytics` - Get analytics data

### WebSocket Endpoint
- `WS /ws/{lobby_id}/{player_id}` - WebSocket connection for real-time game

## WebSocket Events

**Client → Server:**
- `start_game` - Start the game
- `submit_answer` - Submit a single answer
- `submit_all_answers` - Submit all answers
- `ping` - Heartbeat

**Server → Client:**
- `connected` - Connection confirmation
- `player_joined` - Player joined lobby
- `game_started` - Game has started
- `player_ready` - Player submitted answers
- `answers_revealed` - Show all answers
- `player_disconnected` - Player left

## Contributing

See [CLAUDE.md](./CLAUDE.md) for project requirements and [RESEARCH.md](./RESEARCH.md) for architecture details.

## License

ISC
