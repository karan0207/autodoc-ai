"use client"

import { useState } from "react"
import { Sidebar } from "@/components/layout/Sidebar"
import { DashboardStats } from "@/components/dashboard/DashboardStats"
import { IngestCard } from "@/components/dashboard/IngestCard"
import { GenerationPanel } from "@/components/dashboard/GenerationPanel"
import { DocViewer } from "@/components/dashboard/DocViewer"
import { Button } from "@/components/ui/button"
import { FileText, ArrowLeft } from "lucide-react"

interface GeneratedDoc {
  id: string
  title: string
  type: string
  content: string
  createdAt: Date
}

export default function Home() {
  const [activeTab, setActiveTab] = useState("dashboard")
  const [jobId, setJobId] = useState("")
  const [documents, setDocuments] = useState<GeneratedDoc[]>([])
  const [selectedDocId, setSelectedDocId] = useState<string | null>(null)

  const handleIngestComplete = (id: string) => {
    setJobId(id)
    setActiveTab("dashboard")
  }

  const handleGenerateComplete = (content: string, type: string) => {
    console.log("handleGenerateComplete called", { content, type })
    const newDoc: GeneratedDoc = {
      id: Math.random().toString(36).substring(7),
      title: `${type.charAt(0).toUpperCase() + type.slice(1)} Documentation`,
      type,
      content,
      createdAt: new Date()
    }
    console.log("Adding new doc:", newDoc)
    setDocuments(prev => {
      const next = [newDoc, ...prev]
      console.log("New documents state:", next)
      return next
    })
    setSelectedDocId(newDoc.id)
    setActiveTab("library")
  }

  const renderContent = () => {
    if (activeTab === "dashboard") {
      return (
        <div className="space-y-8">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-zinc-900">Dashboard</h1>
            <p className="text-zinc-500">Overview of your documentation generation.</p>
          </div>
          
          <DashboardStats />
          
          <div className="grid gap-8 md:grid-cols-2">
            <div className="space-y-6">
              <h2 className="text-xl font-semibold tracking-tight">Quick Actions</h2>
              {jobId ? (
                <GenerationPanel jobId={jobId} onGenerate={handleGenerateComplete} />
              ) : (
                <div className="p-6 border border-dashed rounded-lg text-center bg-zinc-50">
                  <p className="text-zinc-500 mb-4">No data source connected.</p>
                  <Button onClick={() => setActiveTab("ingest")}>Connect Source</Button>
                </div>
              )}
            </div>
            
            <div className="space-y-6">
              <h2 className="text-xl font-semibold tracking-tight">Recent Activity</h2>
              <div className="space-y-4">
                {documents.length === 0 ? (
                  <p className="text-sm text-zinc-500">No documents generated yet.</p>
                ) : (
                  documents.slice(0, 5).map(doc => (
                    <div key={doc.id} className="flex items-center justify-between p-4 bg-white border rounded-lg shadow-sm cursor-pointer hover:border-indigo-300 transition-colors" onClick={() => { setSelectedDocId(doc.id); setActiveTab("library"); }}>
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-indigo-50 rounded-md">
                          <FileText className="w-4 h-4 text-indigo-600" />
                        </div>
                        <div>
                          <p className="font-medium text-sm">{doc.title}</p>
                          <p className="text-xs text-zinc-500">{doc.createdAt.toLocaleTimeString()}</p>
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>
      )
    }

    if (activeTab === "ingest") {
      return (
        <div className="max-w-4xl mx-auto space-y-8">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-zinc-900">Ingest Sources</h1>
            <p className="text-zinc-500">Connect your website and repository to start generating.</p>
          </div>
          <IngestCard onIngestComplete={handleIngestComplete} />
        </div>
      )
    }

    if (activeTab === "library") {
      if (selectedDocId) {
        const doc = documents.find(d => d.id === selectedDocId)
        if (!doc) return null
        return (
          <div className="h-[calc(100vh-4rem)] flex flex-col">
            <div className="mb-4 flex items-center gap-2">
              <Button variant="ghost" size="sm" onClick={() => setSelectedDocId(null)}>
                <ArrowLeft className="w-4 h-4 mr-1" /> Back to Library
              </Button>
            </div>
            <div className="flex-1 min-h-0">
              <DocViewer content={doc.content} title={doc.title} />
            </div>
          </div>
        )
      }

      return (
        <div className="space-y-8">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-zinc-900">Library</h1>
            <p className="text-zinc-500">Manage and view your generated documentation.</p>
          </div>
          
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {documents.map(doc => (
              <div key={doc.id} className="group relative flex flex-col justify-between p-6 bg-white border rounded-xl shadow-sm hover:shadow-md transition-all cursor-pointer" onClick={() => setSelectedDocId(doc.id)}>
                <div className="space-y-4">
                  <div className="w-10 h-10 rounded-lg bg-indigo-50 flex items-center justify-center group-hover:bg-indigo-100 transition-colors">
                    <FileText className="w-5 h-5 text-indigo-600" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-zinc-900">{doc.title}</h3>
                    <p className="text-sm text-zinc-500 mt-1 line-clamp-2">
                      {doc.content.slice(0, 100)}...
                    </p>
                  </div>
                </div>
                <div className="mt-6 pt-4 border-t flex items-center justify-between text-xs text-zinc-500">
                  <span>{doc.type.toUpperCase()}</span>
                  <span>{doc.createdAt.toLocaleDateString()}</span>
                </div>
              </div>
            ))}
            {documents.length === 0 && (
               <div className="col-span-full text-center py-12 text-zinc-500">
                 No documents found. Go to Dashboard to generate one.
               </div>
            )}
          </div>
        </div>
      )
    }

    return <div className="p-8">Work in progress...</div>
  }

  return (
    <div className="flex min-h-screen bg-zinc-50">
      <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />
      <main className="flex-1 p-8 overflow-y-auto h-screen">
        {renderContent()}
      </main>
    </div>
  )
}
