# Sartel.io - Research & Architecture Plan

## Executive Summary

This document outlines the research findings and technical architecture for implementing Sartel.io, a real-time multiplayer word game. The research phase has identified optimal technology choices, architecture patterns, and implementation strategies aligned with the project requirements.

---

## 1. Current State

**Codebase Status**: Initial stage - only CLAUDE.md requirements file exists
**Git Branch**: `claude/research-project-requirements-01LtXF4s9RtAXdGo2Swoe6fJ`
**Status**: Ready for implementation

---

## 2. Technology Stack Analysis

### Backend: FastAPI + WebSockets

**Why FastAPI**:
- Built on ASGI, which natively supports asynchronous protocols like WebSockets
- No third-party libraries required (unlike Flask-SocketIO or Django Channels)
- Excellent async/await integration for efficient concurrency
- Minimal boilerplate through Starlette integration
- Production-ready for real-time multiplayer games

**WebSocket Architecture Recommendations**:
- **Connection Management**: Group connections by lobby ID for targeted messaging
- **Message Broadcasting**: Use Redis Pub/Sub for coordinating events across multiple server instances
- **Connection Sharding**: Shard connections by lobby to reduce broadcast overhead
- **Background Tasks**: Offload CPU-intensive tasks to Celery or background workers to keep WebSocket event loop responsive

**Key References**:
- [The Secret to Real Time Power: Incorporating WebSockets with FastAPI](https://hexshift.medium.com/the-secret-to-real-time-power-incorporating-websockets-with-fastapi-722e1b64246d)
- [Real-Time FastAPI Chat with Redis Streams and WebSocket Multiplexing](https://medium.com/@connect.hashblock/real-time-fastapi-chat-with-redis-streams-and-websocket-multiplexing-1508b355b9f6)
- [Top Ten Advanced Techniques for Scaling WebSocket Applications with FastAPI](https://hexshift.medium.com/top-ten-advanced-techniques-for-scaling-websocket-applications-with-fastapi-a5af1e5e901f)

### Storage: Redis vs In-Memory

**Recommendation: Redis (with fallback to in-memory for local dev)**

**Why Redis**:
- In-memory database with near-instantaneous access (single-digit milliseconds)
- Built-in TTL (Time-To-Live) for automatic session expiration
- Redis Pub/Sub enables coordination across multiple FastAPI instances
- Horizontal scaling support when using multiple Railway instances
- Lower infrastructure costs due to reduced database reads

**When Redis Wins**:
- Reads dominate writes (✅ perfect for our lobby/game state use case)
- Same payload reused across sessions (✅ lobby state shared between 2 players)
- Need for automatic expiration (✅ ephemeral lobbies)

**Implementation Strategy**:
```python
# Use Redis in production (Railway)
# Use in-memory dict for local development
# Both implementations behind same interface
```

**Key References**:
- [Using Redis with FastAPI](https://redis.io/learn/develop/python/fastapi)
- [Caching with Redis: Boost Your FastAPI Applications](https://mahdijafaridev.medium.com/caching-with-redis-boost-your-fastapi-applications-with-speed-and-scalability-af45626a57f3)
- [fastapi-redis-session](https://pypi.org/project/fastapi-redis-session/)

### Frontend: React + Vite + Shadcn UI

**Setup Recommendations**:

1. **Use TypeScript Template** (recommended for type safety)
   ```bash
   npm create vite@latest frontend -- --template react-ts
   ```

2. **Configure Path Aliases** - Edit both `tsconfig.json` and `tsconfig.app.json`
   - Add `baseUrl` and `paths` for `@/*` imports

3. **Tailwind CSS with Vite Plugin**
   ```bash
   npm install tailwindcss @tailwindcss/vite
   ```

4. **Shadcn UI Initialization**
   ```bash
   npx shadcn@latest init
   ```
   - May require `--force` flag due to React 19 peer dependencies
   - CLI auto-verifies Vite and Tailwind v4 setup

**Component Strategy for Sartel.io**:
- **Table Component**: Use Shadcn's Table for category grid
- **Input Components**: Use Shadcn's Input with auto-focus on Enter
- **Timer Component**: Custom component with real-time WebSocket updates
- **Dialog/Modal**: For lobby creation and join flows
- **Button Components**: For game actions

**Key References**:
- [Vite - shadcn/ui Official Installation](https://ui.shadcn.com/docs/installation/vite)
- [Set Up a Modern React + TypeScript + Tailwind + ShadCN UI App with Vite](https://blog.jubayer.me/2025/07/02/set-up-a-modern-react-typescript-tailwind-shadcn-ui-app-with-vite/)
- [How to Set Up Shadcn UI with React, Vite, and JavaScript (Latest Guide)](https://anuragaffection.medium.com/how-to-set-up-shadcn-ui-with-react-vite-and-javascript-using-npm-npx-latest-guide-3475970d1cb3)

### Deployment: Railway

**Monorepo Configuration**:

Railway supports **Isolated Monorepos** (perfect for our Python backend + JS frontend structure).

**Setup Strategy**:
- **Two Services**: Backend and Frontend as separate Railway services
- **Root Directories**:
  - Backend: `/backend` or `/api`
  - Frontend: `/frontend`
- **Watch Paths**: Configure to prevent cross-triggering rebuilds
  - Backend watch: `/backend/**`
  - Frontend watch: `/frontend/**`

**Configuration Files**:
- `railway.toml` or `railway.json` for service definitions
- Supports automatic deployments on push to main branch

**Available Templates to Reference**:
- FastAPI-React-PGDB template
- FastAPI-React-MongoDB template
- Full Stack FastAPI Template

**Key References**:
- [Deploy a FastAPI App | Railway Docs](https://docs.railway.com/guides/fastapi)
- [Deploying a Monorepo | Railway Docs](https://docs.railway.com/guides/monorepo)
- [Deploy FastAPI-React-PGDB](https://railway.com/deploy/fastapi-react-pgdb)

---

## 3. Recommended Architecture

### Project Structure

```
sartel.io/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── websocket.py         # WebSocket connection manager
│   │   ├── models.py            # Pydantic models
│   │   ├── game/
│   │   │   ├── lobby.py         # Lobby management
│   │   │   ├── game_state.py   # Game state logic
│   │   │   └── categories.py   # Category/letter logic
│   │   ├── storage/
│   │   │   ├── redis_store.py  # Redis implementation
│   │   │   └── memory_store.py # In-memory fallback
│   │   └── analytics.py         # Simple analytics tracking
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── GameTable.tsx   # Main game grid
│   │   │   ├── Timer.tsx       # Shared timer
│   │   │   ├── Lobby.tsx       # Lobby creation/join
│   │   │   └── ScoreCard.tsx   # Self-judging interface
│   │   ├── hooks/
│   │   │   └── useWebSocket.ts # WebSocket connection hook
│   │   ├── lib/
│   │   │   └── utils.ts        # Shadcn utilities
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── Dockerfile
├── railway.toml                 # Railway configuration
├── .gitignore
├── CLAUDE.md
└── RESEARCH.md
```

### Data Models

**Lobby**:
```python
{
    "lobby_id": str,          # 5-character random code
    "players": [str, str],    # Max 2 player IDs
    "state": str,             # "waiting" | "playing" | "reviewing" | "completed"
    "created_at": datetime,
    "expires_at": datetime
}
```

**GameState**:
```python
{
    "lobby_id": str,
    "round_number": int,
    "selected_letter": str,
    "categories": List[str],
    "player_answers": {
        "player1_id": {category: answer},
        "player2_id": {category: answer}
    },
    "timer_started_at": datetime,
    "timer_duration": 60
}
```

**Analytics** (Simple tracking):
```python
{
    "total_lobbies_created": int,
    "total_players": int,
    "total_words_created": int,
    "daily_stats": {...}
}
```

### WebSocket Events

**Client → Server**:
- `create_lobby` → Returns lobby_id
- `join_lobby` → { lobby_id }
- `start_game` → Trigger game start
- `submit_answer` → { category, answer }
- `mark_complete` → Signal ready to review
- `self_judge` → { category, valid: bool }

**Server → Client**:
- `lobby_created` → { lobby_id }
- `player_joined` → { player_count }
- `game_started` → { letter, categories, timer_start }
- `timer_tick` → { remaining_seconds }
- `timer_expired` → Trigger answer reveal
- `answers_revealed` → { player1_answers, player2_answers }
- `opponent_ready` → Player marked answers complete

### Component Flow

1. **Lobby Creation**:
   - User clicks "Create Lobby"
   - Backend generates 5-char code, creates Redis entry with TTL
   - Returns lobby_id to client
   - User shares code with friend

2. **Game Start**:
   - Both players in lobby
   - Either player triggers "Start Game"
   - Backend selects random letter
   - WebSocket broadcasts `game_started` to both players
   - Timer starts synchronously

3. **Gameplay**:
   - Players type answers in table cells
   - On Enter, move to next cell
   - Answers stored locally (not sent until timer expires)
   - Timer ticks broadcast every second

4. **Review Phase**:
   - Timer expires
   - Clients auto-submit all answers via WebSocket
   - Backend broadcasts both players' answers
   - Players self-judge (checkmark valid words)
   - Tally shown

---

## 4. Implementation Priorities

### Phase 1: Core Infrastructure (MVP)
1. Backend setup with FastAPI + WebSocket
2. In-memory storage for lobbies/game state
3. Frontend setup with React + Vite + Shadcn
4. Basic lobby creation and joining
5. WebSocket connection establishment

### Phase 2: Game Mechanics
1. Random letter selection
2. Category table rendering
3. Shared timer implementation
4. Answer submission flow
5. Answer reveal and self-judging

### Phase 3: Production Ready
1. Redis integration for storage
2. Analytics tracking
3. Railway deployment configuration
4. CI/CD pipeline (auto-deploy on main branch push)
5. Error handling and edge cases

### Phase 4: Polish
1. Responsive design
2. Loading states
3. Disconnect handling
4. Lobby expiration cleanup
5. Basic unit tests

---

## 5. Lean Dependencies

### Backend (requirements.txt)
```txt
fastapi==0.115.0
uvicorn[standard]==0.32.0
websockets==13.1
redis==5.2.0              # Only if using Redis
pydantic==2.10.0
python-dotenv==1.0.0
```

### Frontend (package.json core dependencies)
```json
{
  "react": "^18.3.0",
  "react-dom": "^18.3.0",
  "vite": "^6.0.0",
  "tailwindcss": "^4.0.0",
  "@tailwindcss/vite": "^4.0.0"
}
```
*Shadcn components added on-demand via CLI*

---

## 6. Testing Strategy

### Backend Tests (Intentional, Non-Verbose)
- `test_lobby_creation.py` - Verify unique lobby IDs
- `test_websocket_connection.py` - Test connection lifecycle
- `test_game_flow.py` - End-to-end game round
- `test_timer_sync.py` - Verify timer broadcasts

### Frontend Tests
- `GameTable.test.tsx` - Cell navigation on Enter
- `useWebSocket.test.ts` - Connection hook behavior
- `Timer.test.tsx` - Countdown display

**Test Philosophy**: Focus on critical paths, avoid over-testing implementation details.

---

## 7. Railway Deployment Configuration

### railway.toml
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
restartPolicyType = "on-failure"

[[services]]
name = "backend"
rootDirectory = "/backend"

[[services]]
name = "frontend"
rootDirectory = "/frontend"

[services.frontend.build]
buildCommand = "npm run build"
startCommand = "npm run preview"
```

### Watch Paths
- Backend: `/backend/**`
- Frontend: `/frontend/**`

---

## 8. Technical Decisions Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Backend Framework** | FastAPI | Native WebSocket support, async-first, minimal boilerplate |
| **Real-time Protocol** | WebSockets | Bidirectional, low-latency, perfect for game state sync |
| **Storage (Prod)** | Redis | Built-in TTL, Pub/Sub for scaling, fast in-memory access |
| **Storage (Dev)** | Python dict | Zero setup for local development |
| **Frontend Framework** | React + Vite | Fast dev experience, modern tooling |
| **UI Library** | Shadcn UI | Unstyled components, full customization, Tailwind-based |
| **Monorepo Style** | Isolated | Separate backend/frontend directories with independent configs |
| **Deployment** | Railway | Native monorepo support, auto-deploy on push, simple config |
| **Language** | TypeScript (FE), Python (BE) | Type safety, modern best practices |

---

## 9. Open Questions / Decisions Needed

1. **Categories List**: Should we have a fixed set or allow custom categories?
   - *Recommendation*: Start with fixed set (8-10 categories) for MVP

2. **Lobby Expiration**: How long should inactive lobbies persist?
   - *Recommendation*: 30 minutes of inactivity, configurable via env var

3. **Analytics Persistence**: How long should we keep analytics?
   - *Recommendation*: Daily aggregates for 30 days (minimal storage)

4. **Letter Selection**: Random from full alphabet or exclude difficult letters (Q, X, Z)?
   - *Recommendation*: Full alphabet for MVP, can add difficulty settings later

5. **Multiple Rounds**: Should lobbies support multiple rounds or one-and-done?
   - *Recommendation*: Support multiple rounds with "Play Again" button

---

## 10. Next Steps

Once research is approved, the implementation will proceed in this order:

1. ✅ Create project structure (backend/ and frontend/ directories)
2. ✅ Initialize FastAPI backend with basic health check
3. ✅ Initialize React + Vite + Shadcn frontend
4. ✅ Set up WebSocket connection manager
5. ✅ Implement lobby creation/joining logic
6. ✅ Build game table UI component
7. ✅ Implement timer synchronization
8. ✅ Add answer submission and reveal
9. ✅ Integrate Redis (with in-memory fallback)
10. ✅ Configure Railway deployment
11. ✅ Add basic tests
12. ✅ Deploy and test in production

---

## 11. Key Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| **WebSocket disconnections** | Game interruption | Implement reconnection logic with state recovery |
| **Timer desync** | Unfair gameplay | Server-authoritative timer, client displays only |
| **Concurrent lobby creation** | ID collisions | Use cryptographically secure random IDs (5 chars = 916M combinations) |
| **Redis unavailability** | Service outage | Graceful fallback to in-memory + health checks |
| **Railway cold starts** | Slow lobby creation | Keep at least 1 instance warm via health checks |

---

## 12. Success Metrics

- **Lobby creation time**: < 500ms
- **WebSocket latency**: < 100ms
- **Timer accuracy**: ± 100ms between clients
- **Deployment time**: < 5 minutes from push to live
- **Test coverage**: > 70% on critical paths

---

## Conclusion

The research phase has validated the technical approach outlined in CLAUDE.md. The combination of FastAPI + WebSockets + Redis + React + Vite + Shadcn UI provides a modern, lean, and scalable foundation for Sartel.io. Railway's native monorepo support simplifies deployment and CI/CD.

**Ready to proceed with implementation.**

---

## Sources

### FastAPI + WebSockets
- [The Secret to Real Time Power: Incorporating WebSockets with FastAPI](https://hexshift.medium.com/the-secret-to-real-time-power-incorporating-websockets-with-fastapi-722e1b64246d)
- [Unlock the Power of WebSockets with FastAPI: Real-Time Apps](https://seenode.com/blog/websockets-with-fastapi-real-time-apps-tutorial/)
- [Real-Time FastAPI Chat with Redis Streams and WebSocket Multiplexing](https://medium.com/@connect.hashblock/real-time-fastapi-chat-with-redis-streams-and-websocket-multiplexing-1508b355b9f6)
- [Top Ten Advanced Techniques for Scaling WebSocket Applications with FastAPI](https://hexshift.medium.com/top-ten-advanced-techniques-for-scaling-websocket-applications-with-fastapi-a5af1e5e901f)
- [FastAPI + WebSockets + React: Real-Time Features](https://medium.com/@suganthi2496/fastapi-websockets-react-real-time-features-for-your-modern-apps-b8042a10fd90)

### Redis Storage
- [Using Redis with FastAPI](https://redis.io/learn/develop/python/fastapi)
- [Caching with Redis: Boost Your FastAPI Applications](https://mahdijafaridev.medium.com/caching-with-redis-boost-your-fastapi-applications-with-speed-and-scalability-af45626a57f3)
- [Building a REST API with FastAPI and Redis Caching](https://medium.com/@suganthi2496/building-a-rest-api-with-fastapi-and-redis-caching-278c4dc07d70)
- [fastapi-redis-session](https://pypi.org/project/fastapi-redis-session/)

### React + Vite + Shadcn UI
- [Vite - shadcn/ui Official Installation](https://ui.shadcn.com/docs/installation/vite)
- [Set Up a Modern React + TypeScript + Tailwind + ShadCN UI App with Vite](https://blog.jubayer.me/2025/07/02/set-up-a-modern-react-typescript-tailwind-shadcn-ui-app-with-vite/)
- [How to Set Up Shadcn UI with React, Vite, and JavaScript (Latest Guide)](https://anuragaffection.medium.com/how-to-set-up-shadcn-ui-with-react-vite-and-javascript-using-npm-npx-latest-guide-3475970d1cb3)
- [How to Use Shadcn UI in Your React + Vite Project](https://medium.com/@sudhanshudeveloper/how-to-use-shadcn-ui-in-your-react-vite-project-31cbf47f6132)

### Railway Deployment
- [Deploy a FastAPI App | Railway Docs](https://docs.railway.com/guides/fastapi)
- [Deploying a Monorepo | Railway Docs](https://docs.railway.com/guides/monorepo)
- [Deploy FastAPI-React-PGDB](https://railway.com/deploy/fastapi-react-pgdb)
- [Deploy FastAPI-React-MongoDB-Template](https://railway.com/deploy/fastapi-react-mongodb-template)
