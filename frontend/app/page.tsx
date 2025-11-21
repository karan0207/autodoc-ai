"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Label } from "@/components/ui/label"

import { toast } from "sonner"

export default function Home() {
  const [url, setUrl] = useState("")
  const [repoUrl, setRepoUrl] = useState("")
  const [loading, setLoading] = useState(false)
  const [jobId, setJobId] = useState("")
  const [status, setStatus] = useState("")
  const [generatedContent, setGeneratedContent] = useState("")
  const [sources, setSources] = useState<any[]>([])
  const [customPrompt, setCustomPrompt] = useState("")

  const handleGenerate = async (type: string, prompt: string) => {
      if (!jobId) return
      setLoading(true)
      setStatus(`Generating ${type}...`)
      setGeneratedContent("")
      
      try {
          const res = await fetch("http://localhost:8000/api/v1/generate", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ job_id: jobId, type, prompt }),
          })
          
          if (!res.ok) throw new Error("Generation failed")
          
          const data = await res.json()
          setGeneratedContent(data.content)
          setSources(data.sources)
          setStatus("Generation complete!")
          toast.success("Documentation generated successfully!")
      } catch (e) {
          console.error(e)
          setStatus("Error generating content")
          toast.error("Failed to generate documentation.")
      }
      setLoading(false)
  }

  const handleIngest = async () => {
    if (!url || !repoUrl) {
      toast.error("Please enter both URLs")
      return
    }
    
    setLoading(true)
    setStatus("Starting ingestion...")
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
      setJobId(data.job_id)
      setStatus("Ingestion started! Check backend logs for progress.")
      toast.success("Ingestion started successfully!")
    } catch (e) {
      console.error(e)
      setStatus("Error starting ingestion")
      toast.error("Failed to start ingestion.")
    }
    setLoading(false)
  }

  return (
    <div className="container mx-auto py-10 flex items-center justify-center min-h-screen bg-gray-50">
      <Card className="w-[500px] shadow-lg">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center">AutoDoc AI</CardTitle>
          <CardDescription className="text-center">Generate documentation from your code and website.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="url">Website URL</Label>
            <Input 
              id="url" 
              placeholder="https://example.com/docs" 
              value={url} 
              onChange={(e) => setUrl(e.target.value)} 
            />
            <p className="text-xs text-gray-500">The root URL of the documentation site.</p>
          </div>
          <div className="space-y-2">
            <Label htmlFor="repo">GitHub Repo URL</Label>
            <Input 
              id="repo" 
              placeholder="https://github.com/owner/repo" 
              value={repoUrl} 
              onChange={(e) => setRepoUrl(e.target.value)} 
            />
            <p className="text-xs text-gray-500">The public GitHub repository URL.</p>
          </div>
          
          <Button onClick={handleIngest} disabled={loading} className="w-full">
            {loading ? "Starting Ingestion..." : "Start Ingestion"}
          </Button>
          
          {status && (
            <div className={`mt-4 p-4 rounded text-sm ${status.includes("Error") ? "bg-red-100 text-red-800" : "bg-green-100 text-green-800"}`}>
              {status}
              {jobId && <div className="font-mono mt-1 text-xs">Job ID: {jobId}</div>}
            </div>
          )}
          
          {jobId && (
            <div className="space-y-4 pt-4 border-t">
                <h3 className="font-semibold">Generate Documentation</h3>
                <div className="grid grid-cols-2 gap-2">
                    <Button variant="outline" onClick={() => handleGenerate("api", "Generate API Reference")}>API Reference</Button>
                    <Button variant="outline" onClick={() => handleGenerate("product", "Generate Product Description")}>Product Desc</Button>
                    <Button variant="outline" onClick={() => handleGenerate("changelog", "Summarize Changelog")}>Changelog</Button>
                    <Button variant="outline" onClick={() => handleGenerate("custom", "Generate SEO Landing Page")}>SEO Page</Button>
                </div>
                
                <div className="space-y-2">
                    <Label>Custom Prompt</Label>
                    <Input 
                        placeholder="e.g., Write a tutorial for the authentication API" 
                        value={customPrompt}
                        onChange={(e) => setCustomPrompt(e.target.value)}
                    />
                    <Button className="w-full" onClick={() => handleGenerate("custom", customPrompt)}>Generate Custom</Button>
                </div>
            </div>
          )}
          
          {generatedContent && (
            <div className="mt-6 pt-4 border-t">
                <div className="flex justify-between items-center mb-2">
                    <h3 className="font-semibold">Generated Output</h3>
                    <div className="space-x-2">
                        <Button variant="outline" size="sm" onClick={() => navigator.clipboard.writeText(generatedContent)}>
                            Copy
                        </Button>
                        <Button variant="outline" size="sm" onClick={() => {
                            const blob = new Blob([generatedContent], { type: 'text/markdown' });
                            const url = URL.createObjectURL(blob);
                            const a = document.createElement('a');
                            a.href = url;
                            a.download = 'documentation.md';
                            a.click();
                        }}>
                            Download MD
                        </Button>
                        <Button variant="outline" size="sm" onClick={() => {
                            const blob = new Blob([JSON.stringify({ content: generatedContent, sources }, null, 2)], { type: 'application/json' });
                            const url = URL.createObjectURL(blob);
                            const a = document.createElement('a');
                            a.href = url;
                            a.download = 'documentation.json';
                            a.click();
                        }}>
                            Download JSON
                        </Button>
                    </div>
                </div>
                <div className="bg-gray-100 p-4 rounded-md whitespace-pre-wrap text-sm max-h-[400px] overflow-y-auto font-mono">
                    {generatedContent}
                </div>
                <div className="mt-2 text-xs text-gray-500">
                    Sources used: {sources.length}
                </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
