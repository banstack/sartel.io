import { useState } from 'react'
import { Home } from './components/Home'
import { Lobby } from './components/Lobby'

function App() {
  const [view, setView] = useState<'home' | 'lobby'>('home')
  const [lobbyId, setLobbyId] = useState<string | null>(null)
  const [playerId, setPlayerId] = useState<string>(() => {
    // Generate or retrieve player ID
    const stored = localStorage.getItem('sartel-player-id')
    if (stored) return stored
    const newId = `player-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
    localStorage.setItem('sartel-player-id', newId)
    return newId
  })

  const handleCreateLobby = async () => {
    try {
      const response = await fetch('/api/lobby/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (!response.ok) {
        throw new Error('Failed to create lobby')
      }

      const data = await response.json()
      setLobbyId(data.lobby_id)
      setView('lobby')
    } catch (error) {
      console.error('Error creating lobby:', error)
      alert('Failed to create lobby. Please try again.')
    }
  }

  const handleJoinLobby = async (code: string) => {
    try {
      const response = await fetch(`/api/lobby/${code}`)

      if (!response.ok) {
        throw new Error('Lobby not found')
      }

      const data = await response.json()

      if (data.lobby.players.length >= 2) {
        alert('Lobby is full')
        return
      }

      setLobbyId(code)
      setView('lobby')
    } catch (error) {
      console.error('Error joining lobby:', error)
      alert('Failed to join lobby. Please check the code and try again.')
    }
  }

  const handleLeaveLobby = () => {
    setLobbyId(null)
    setView('home')
  }

  return (
    <div className="min-h-screen bg-background">
      {view === 'home' && (
        <Home onCreateLobby={handleCreateLobby} onJoinLobby={handleJoinLobby} />
      )}

      {view === 'lobby' && lobbyId && (
        <Lobby
          lobbyId={lobbyId}
          playerId={playerId}
          onLeave={handleLeaveLobby}
        />
      )}
    </div>
  )
}

export default App
