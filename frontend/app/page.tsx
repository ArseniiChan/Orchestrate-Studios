"use client"

import { useState, useEffect } from "react"
import { Moon, Sun } from "lucide-react"
import { DashboardLayout } from "@/components/dashboard-layout"
import { VideoUploader } from "@/components/video-uploader"
import { OrchestrationStatus } from "@/components/orchestration-status"
import { CampaignResults } from "@/components/campaign-results"
import { ExportManager } from "@/components/export-manager"
import { Button } from "@/components/ui/button"

export default function Home() {
  const [isDark, setIsDark] = useState(false)
  const [mounted, setMounted] = useState(false)
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [orchStatus, setOrchStatus] = useState<"idle" | "uploading" | "orchestrating" | "completed" | "error">("idle")
  const [campaignData, setCampaignData] = useState<any>(null)

  useEffect(() => {
    setMounted(true)
    const isDarkMode =
      localStorage.getItem("theme") === "dark" ||
      (!localStorage.getItem("theme") && window.matchMedia("(prefers-color-scheme: dark)").matches)
    setIsDark(isDarkMode)
    updateTheme(isDarkMode)
  }, [])

  const updateTheme = (dark: boolean) => {
    const html = document.documentElement
    if (dark) {
      html.classList.add("dark")
      localStorage.setItem("theme", "dark")
    } else {
      html.classList.remove("dark")
      localStorage.setItem("theme", "light")
    }
  }

  const toggleTheme = () => {
    const newIsDark = !isDark
    setIsDark(newIsDark)
    updateTheme(newIsDark)
  }

  const resetCampaign = () => {
    setUploadedFile(null)
    setOrchStatus("idle")
    setCampaignData(null)
  }

  if (!mounted) return null

  return (
    <DashboardLayout>
      <div className="min-h-screen bg-background">
        {/* Header */}
        <div className="sticky top-0 z-40 border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
          <div className="flex items-center justify-between px-6 py-4">
            <div>
              <h1 className="text-2xl font-bold text-foreground">Marketing Operations</h1>
              <p className="text-sm text-muted-foreground">AI-Powered Content Generation Pipeline</p>
            </div>
            <div className="flex items-center gap-3">
              {campaignData && (
                <Button
                  variant="outline"
                  onClick={resetCampaign}
                  className="text-muted-foreground hover:text-foreground bg-transparent"
                >
                  Start New Campaign
                </Button>
              )}
              <Button variant="outline" size="icon" onClick={toggleTheme} className="rounded-full bg-transparent">
                {isDark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
              </Button>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="px-6 py-8">
          <div className="space-y-8">
            {/* Video Upload Section */}
            <VideoUploader onFileSelect={setUploadedFile} onStatusChange={setOrchStatus} />

            {/* Orchestration Status */}
            {uploadedFile && (
              <OrchestrationStatus
                status={orchStatus}
                onComplete={(data) => {
                  setCampaignData(data)
                  setOrchStatus("completed")
                }}
              />
            )}

            {/* Campaign Results */}
            {campaignData && orchStatus === "completed" && (
              <>
                <CampaignResults data={campaignData} />
                <ExportManager campaignData={campaignData} />
              </>
            )}
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}
