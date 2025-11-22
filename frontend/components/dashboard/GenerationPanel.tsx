import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Wand2, FileCode, FileText, History, Sparkles } from "lucide-react"
import { toast } from "sonner"

interface GenerationPanelProps {
  jobId: string
  onGenerate: (content: string, type: string) => void
}

export function GenerationPanel({ jobId, onGenerate }: GenerationPanelProps) {
  const [loading, setLoading] = useState(false)
  const [customPrompt, setCustomPrompt] = useState("")

  const handleGenerate = async (type: string, prompt: string) => {
      if (!jobId) {
        toast.error("No active job. Please ingest data first.")
        return
      }
      setLoading(true)
      
      try {
          const res = await fetch("http://localhost:8000/api/v1/generate", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ job_id: jobId, type, prompt }),
          })
          
          if (!res.ok) throw new Error("Generation failed")
          
          const data = await res.json()
          console.log("Generation successful, data:", data)
          onGenerate(data.content, type)
          toast.success("Documentation generated successfully!")
      } catch (e) {
          console.error(e)
          toast.error("Failed to generate documentation.")
      }
      setLoading(false)
  }

  return (
    <Card className="w-full shadow-sm border-zinc-200">
      <CardHeader>
        <CardTitle className="text-lg font-semibold flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-indigo-500" />
            Generate Documentation
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Button 
                variant="outline" 
                className="h-24 flex flex-col items-center justify-center gap-2 hover:border-indigo-500 hover:bg-indigo-50"
                onClick={() => handleGenerate("api", "Generate API Reference")}
                disabled={loading}
            >
                <FileCode className="w-6 h-6 text-zinc-600" />
                <span>API Reference</span>
            </Button>
            <Button 
                variant="outline" 
                className="h-24 flex flex-col items-center justify-center gap-2 hover:border-indigo-500 hover:bg-indigo-50"
                onClick={() => handleGenerate("product", "Generate Product Description")}
                disabled={loading}
            >
                <FileText className="w-6 h-6 text-zinc-600" />
                <span>Product Guide</span>
            </Button>
            <Button 
                variant="outline" 
                className="h-24 flex flex-col items-center justify-center gap-2 hover:border-indigo-500 hover:bg-indigo-50"
                onClick={() => handleGenerate("changelog", "Summarize Changelog")}
                disabled={loading}
            >
                <History className="w-6 h-6 text-zinc-600" />
                <span>Changelog</span>
            </Button>
            <Button 
                variant="outline" 
                className="h-24 flex flex-col items-center justify-center gap-2 hover:border-indigo-500 hover:bg-indigo-50"
                onClick={() => handleGenerate("custom", "Generate SEO Landing Page")}
                disabled={loading}
            >
                <Wand2 className="w-6 h-6 text-zinc-600" />
                <span>SEO Landing Page</span>
            </Button>
        </div>
        
        <div className="space-y-2 pt-4 border-t">
            <Label>Custom Prompt</Label>
            <div className="flex gap-2">
                <Input 
                    placeholder="e.g., Write a tutorial for the authentication API" 
                    value={customPrompt}
                    onChange={(e) => setCustomPrompt(e.target.value)}
                />
                <Button onClick={() => handleGenerate("custom", customPrompt)} disabled={loading}>
                    Generate
                </Button>
            </div>
        </div>
      </CardContent>
    </Card>
  )
}
