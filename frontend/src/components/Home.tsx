import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

interface HomeProps {
  onCreateLobby: () => void
  onJoinLobby: (lobbyId: string) => void
}

export function Home({ onCreateLobby, onJoinLobby }: HomeProps) {
  const [joinCode, setJoinCode] = useState('')

  const handleJoin = () => {
    if (joinCode.trim()) {
      onJoinLobby(joinCode.toUpperCase().trim())
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-4xl space-y-8">
        <div className="text-center space-y-2">
          <h1 className="text-6xl font-bold tracking-tight">Sartel.io</h1>
          <p className="text-xl text-muted-foreground">
            The Real-Time Word Game
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle>Create Lobby</CardTitle>
              <CardDescription>
                Start a new game and invite a friend
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button onClick={onCreateLobby} className="w-full" size="lg">
                Create New Lobby
              </Button>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle>Join Lobby</CardTitle>
              <CardDescription>
                Enter a lobby code to join an existing game
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <Input
                placeholder="Enter lobby code"
                value={joinCode}
                onChange={(e) => setJoinCode(e.target.value.toUpperCase())}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    handleJoin()
                  }
                }}
                maxLength={5}
                className="uppercase text-center text-lg font-mono"
              />
              <Button
                onClick={handleJoin}
                disabled={!joinCode.trim()}
                className="w-full"
                size="lg"
              >
                Join Game
              </Button>
            </CardContent>
          </Card>
        </div>

        <div className="text-center text-sm text-muted-foreground">
          <p>How to play:</p>
          <p>
            Two players compete to come up with words starting with a random
            letter for each category
          </p>
        </div>
      </div>
    </div>
  )
}
