import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"

import { LayoutDashboard, Library, UploadCloud, Settings, FileText, PlusCircle } from "lucide-react"

interface SidebarProps extends React.HTMLAttributes<HTMLDivElement> {
  activeTab: string
  onTabChange: (tab: string) => void
}

export function Sidebar({ className, activeTab, onTabChange }: SidebarProps) {
  return (
    <div className={cn("pb-12 w-64 border-r bg-zinc-950 text-white min-h-screen relative", className)}>
      <div className="space-y-4 py-4">
        <div className="px-3 py-2">
          <h2 className="mb-2 px-4 text-lg font-semibold tracking-tight text-indigo-400 flex items-center gap-2">
            <FileText className="w-5 h-5" />
            AutoDoc AI
          </h2>
          <div className="space-y-1">
            <Button 
              variant={activeTab === "dashboard" ? "secondary" : "ghost"} 
              className="w-full justify-start" 
              onClick={() => onTabChange("dashboard")}
            >
              <LayoutDashboard className="mr-2 h-4 w-4" />
              Dashboard
            </Button>
            <Button 
              variant={activeTab === "library" ? "secondary" : "ghost"} 
              className="w-full justify-start"
              onClick={() => onTabChange("library")}
            >
              <Library className="mr-2 h-4 w-4" />
              Library
            </Button>
            <Button 
              variant={activeTab === "ingest" ? "secondary" : "ghost"} 
              className="w-full justify-start"
              onClick={() => onTabChange("ingest")}
            >
              <UploadCloud className="mr-2 h-4 w-4" />
              Ingest Sources
            </Button>
            <Button 
              variant={activeTab === "settings" ? "secondary" : "ghost"} 
              className="w-full justify-start"
              onClick={() => onTabChange("settings")}
            >
              <Settings className="mr-2 h-4 w-4" />
              Settings
            </Button>
          </div>
        </div>
        <div className="px-3 py-2">
          <h2 className="mb-2 px-4 text-lg font-semibold tracking-tight">
            Recent
          </h2>
          <div className="space-y-1">
            <Button variant="ghost" className="w-full justify-start text-zinc-400 hover:text-white">
              <FileText className="mr-2 h-4 w-4" />
              API Reference v1
            </Button>
            <Button variant="ghost" className="w-full justify-start text-zinc-400 hover:text-white">
              <FileText className="mr-2 h-4 w-4" />
              Product Guide
            </Button>
          </div>
        </div>
      </div>
      <div className="px-3 py-2 mt-auto absolute bottom-0 w-full">
         <Button className="w-full bg-indigo-600 hover:bg-indigo-700 text-white">
            <PlusCircle className="mr-2 h-4 w-4" />
            New Project
         </Button>
      </div>
    </div>
  )
}
