'use client'

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { signInWithLinkedIn } from "./actions"
import { useEffect, useState } from "react"
import { createClient } from "@/utils/supabase/client"
import { User } from "@supabase/supabase-js"


export function LoginScreen() {
  const [user, setUser] = useState<User | null>(null)
  const supabase = createClient()

  useEffect(() => {
    const fetchUser = async () => {
      const { data: { user } } = await supabase.auth.getUser()
      setUser(user ?? null)
    }
    fetchUser()

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null)
    })

    return () => subscription.unsubscribe()
  }, [supabase])

  const handleLinkedInSignIn = async () => {
    const result = await signInWithLinkedIn()
    if (result && 'error' in result) {
      const { error } = result
      // Handle error (e.g., show error message to user)
      console.error('Error signing in with LinkedIn:', error)
    }
  }

  return (
    <div>
      <div className="flex items-center justify-center min-h-screen bg-gray-100">
        {user ? (
          <Card className="flex flex-col items-center justify-center gap-4 p-4">
            <p>Welcome, {user.email}</p>
            <Button onClick={() => supabase.auth.signOut()}>Sign out</Button>
          </Card>
        ) : (
          <Card className="w-full max-w-md">
            <CardHeader className="space-y-1">
              <CardTitle className="text-2xl font-bold text-center">Login</CardTitle>
              <CardDescription className="text-center">
                Choose your login method
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Button
                variant="outline"
                className="w-full h-12 text-lg font-medium"
                onClick={handleLinkedInSignIn}
              >
                <img
                  src="/auth-logos/linkedin.png"
                  alt="Sign in with LinkedIn"
                  style={{ maxWidth: '100%', maxHeight: '70%' }}
                />
                <span className="ml-4 text-lg font-medium">Sign in with LinkedIn</span>
              </Button>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}