import { useState } from 'react'
import { useWebSocket } from '@/hooks/useWebSocket'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

interface LobbyProps {
  lobbyId: string
  playerId: string
  onLeave: () => void
}

export function Lobby({ lobbyId, playerId, onLeave }: LobbyProps) {
  const [players, setPlayers] = useState<string[]>([])
  const [playerCount, setPlayerCount] = useState(0)
  const [gameStarted, setGameStarted] = useState(false)

  const { isConnected, sendMessage } = useWebSocket(
    lobbyId,
    playerId,
    {
      onMessage: (message) => {
        console.log('Received message:', message)

        switch (message.type) {
          case 'connected':
            console.log('Connected to lobby')
            break
          case 'player_joined':
            setPlayerCount(message.player_count as number)
            setPlayers(message.players as string[])
            break
          case 'game_started':
            setGameStarted(true)
            break
          case 'player_disconnected':
            setPlayerCount(message.player_count as number)
            break
        }
      },
      onOpen: () => {
        console.log('WebSocket connected')
      },
      onClose: () => {
        console.log('WebSocket disconnected')
      },
    }
  )

  const handleStartGame = () => {
    sendMessage({ type: 'start_game' })
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <Card className="w-full max-w-2xl">
        <CardHeader>
          <CardTitle>Lobby: {lobbyId}</CardTitle>
          <CardDescription>
            Share this code with your friend to join
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-secondary rounded-lg">
            <div>
              <p className="text-sm font-medium">Connection Status</p>
              <p className="text-2xl font-bold">
                {isConnected ? (
                  <span className="text-green-600">Connected</span>
                ) : (
                  <span className="text-red-600">Disconnected</span>
                )}
              </p>
            </div>
            <div>
              <p className="text-sm font-medium">Players</p>
              <p className="text-2xl font-bold">{playerCount}/2</p>
            </div>
          </div>

          {players.length > 0 && (
            <div className="space-y-2">
              <p className="text-sm font-medium">Connected Players:</p>
              <ul className="space-y-1">
                {players.map((player, index) => (
                  <li
                    key={player}
                    className="p-2 bg-secondary rounded flex items-center justify-between"
                  >
                    <span>Player {index + 1}</span>
                    {player === playerId && (
                      <span className="text-sm text-muted-foreground">(You)</span>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {!gameStarted && (
            <div className="flex gap-2">
              <Button
                onClick={handleStartGame}
                disabled={playerCount !== 2 || !isConnected}
                className="flex-1"
              >
                Start Game
              </Button>
              <Button onClick={onLeave} variant="outline">
                Leave Lobby
              </Button>
            </div>
          )}

          {gameStarted && (
            <div className="text-center p-8 bg-secondary rounded-lg">
              <p className="text-2xl font-bold">Game Started!</p>
              <p className="text-sm text-muted-foreground mt-2">
                Game interface will be implemented in Phase 2
              </p>
            </div>
          )}

          {playerCount < 2 && !gameStarted && (
            <div className="text-center p-4 bg-yellow-100 dark:bg-yellow-900/20 rounded-lg">
              <p className="text-sm">
                Waiting for another player to join...
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
