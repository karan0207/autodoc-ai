import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Globe, Github, Loader2 } from "lucide-react"
import { toast } from "sonner"

interface IngestCardProps {
  onIngestComplete: (jobId: string) => void
}

export function IngestCard({ onIngestComplete }: IngestCardProps) {
  const [url, setUrl] = useState("")
  const [repoUrl, setRepoUrl] = useState("")
  const [loading, setLoading] = useState(false)

  const handleIngest = async () => {
    if (!url || !repoUrl) {
      toast.error("Please enter both URLs")
      return
    }
    
    setLoading(true)
    try {
      const res = await fetch("http://localhost:8000/api/v1/ingest", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url, repo_url: repoUrl }),
      })
      
      if (!res.ok) {
        throw new Error("Failed to start ingestion")
      }
      
      const data = await res.json()
      onIngestComplete(data.job_id)
      toast.success("Ingestion started successfully!")
    } catch (e) {
      console.error(e)
      toast.error("Failed to start ingestion.")
    }
    setLoading(false)
  }

  return (
    <Card className="w-full max-w-2xl mx-auto shadow-md border-zinc-200">
      <CardHeader>
        <CardTitle className="text-xl font-bold">Add Data Sources</CardTitle>
        <CardDescription>Connect your documentation and code repository.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="grid gap-6 md:grid-cols-2">
          <div className="space-y-2">
            <Label htmlFor="url" className="flex items-center gap-2">
              <Globe className="w-4 h-4 text-indigo-500" />
              Website URL
            </Label>
            <Input 
              id="url" 
              placeholder="https://example.com/docs" 
              value={url} 
              onChange={(e) => setUrl(e.target.value)} 
              className="bg-zinc-50 border-zinc-200 focus:ring-indigo-500"
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="repo" className="flex items-center gap-2">
              <Github className="w-4 h-4 text-zinc-900" />
              GitHub Repo
            </Label>
            <Input 
              id="repo" 
              placeholder="https://github.com/owner/repo" 
              value={repoUrl} 
              onChange={(e) => setRepoUrl(e.target.value)} 
              className="bg-zinc-50 border-zinc-200 focus:ring-indigo-500"
            />
          </div>
        </div>
        
        <Button 
          onClick={handleIngest} 
          disabled={loading} 
          className="w-full bg-indigo-600 hover:bg-indigo-700 text-white"
        >
          {loading ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Ingesting...
            </>
          ) : (
            "Start Ingestion"
          )}
        </Button>
      </CardContent>
    </Card>
  )
}
