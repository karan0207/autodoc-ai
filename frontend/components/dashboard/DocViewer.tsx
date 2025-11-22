import React from 'react'
import ReactMarkdown from 'react-markdown'
import { Button } from "@/components/ui/button"
import { Download, Copy, Check } from "lucide-react"
import { toast } from "sonner"

interface DocViewerProps {
  content: string
  title?: string
}

export function DocViewer({ content, title = "Generated Documentation" }: DocViewerProps) {
  const [copied, setCopied] = React.useState(false)

  const handleCopy = () => {
    navigator.clipboard.writeText(content)
    setCopied(true)
    toast.success("Copied to clipboard")
    setTimeout(() => setCopied(false), 2000)
  }

  const handleDownload = () => {
    const blob = new Blob([content], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${title.replace(/\s+/g, '_').toLowerCase()}.md`
    a.click()
  }

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-sm border border-zinc-200 overflow-hidden">
      <div className="flex items-center justify-between px-4 py-3 border-b bg-zinc-50">
        <h3 className="font-medium text-zinc-900">{title}</h3>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" onClick={handleCopy} className="h-8 w-8 p-0">
            {copied ? <Check className="h-4 w-4 text-green-500" /> : <Copy className="h-4 w-4 text-zinc-500" />}
          </Button>
          <Button variant="ghost" size="sm" onClick={handleDownload} className="h-8 w-8 p-0">
            <Download className="h-4 w-4 text-zinc-500" />
          </Button>
        </div>
      </div>
      <div className="flex-1 overflow-y-auto p-6 bg-white">
        <article className="prose prose-zinc max-w-none dark:prose-invert">
          <ReactMarkdown>{content}</ReactMarkdown>
        </article>
      </div>
    </div>
  )
}
