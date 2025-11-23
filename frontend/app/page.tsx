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
    
    // Check for stored campaign data on mount
    const stored = localStorage.getItem('lastCampaign')
    if (stored && !campaignData) {
      try {
        const data = JSON.parse(stored)
        console.log("Restored campaign data from storage")
        setCampaignData(data)
        setOrchStatus("completed")
      } catch (e) {
        console.error("Failed to restore campaign data:", e)
      }
    }
  }, [])

  // Prevent data loss
  useEffect(() => {
    if (campaignData && campaignData.strategy) {
      console.log("Storing campaign data to localStorage")
      localStorage.setItem('lastCampaign', JSON.stringify(campaignData))
    }
  }, [campaignData])

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
    localStorage.removeItem('lastCampaign')
  }

  // FIXED: Handler for when campaign is created with validation
  const handleCampaignCreated = (data: any) => {
    console.log("Campaign created in page.tsx:", data)
    
    // Validate the data before setting
    if (data && data.strategy && data.platform_content) {
      console.log("Valid campaign data received, updating state")
      setCampaignData(data)
      setOrchStatus("completed")
    } else if (data) {
      console.warn("Campaign data might be incomplete:", {
        hasStrategy: !!data.strategy,
        hasPlatformContent: !!data.platform_content,
        hasProductionTasks: !!data.production_tasks
      })
      // Still set it even if partially complete
      setCampaignData(data)
      setOrchStatus("completed")
    } else {
      console.error("Invalid or empty campaign data received")
    }
  }

  if (!mounted) return null

  return (
    <DashboardLayout>
      <div className="min-h-screen bg-background">
        {/* Header */}
        <div className="sticky top-0 z-40 border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
          <div className="flex items-center justify-between px-6 py-4">
            <div>
              <h1 className="text-2xl font-bold text-foreground">Marketing Operations Command Center</h1>
              <p className="text-sm text-muted-foreground">IBM watsonx Orchestrate - Transform Videos into Campaigns in 3 Minutes</p>
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
            {/* Video Uploader with campaign handler */}
            <VideoUploader 
              onFileSelect={setUploadedFile} 
              onStatusChange={setOrchStatus}
              onCampaignCreated={handleCampaignCreated}
            />

            {/* Orchestration Status - Only show when processing */}
            {uploadedFile && orchStatus !== "idle" && orchStatus !== "completed" && (
              <OrchestrationStatus
                status={orchStatus}
                onComplete={(data) => {
                  // Prevent overwriting existing campaign data
                  if (!campaignData && data) {
                    console.log("OrchestrationStatus providing data:", data)
                    setCampaignData(data)
                    setOrchStatus("completed")
                  } else if (campaignData) {
                    console.log("Campaign data already exists, skipping OrchestrationStatus update")
                  }
                }}
              />
            )}

            {/* Campaign Results - Show when we have campaign data */}
            {campaignData && (
              <>
                {console.log("Rendering with campaign data:", {
                  hasStrategy: !!campaignData.strategy,
                  hasPlatformContent: !!campaignData.platform_content,
                  transcriptLength: campaignData.transcript?.length || 0
                })}
                
                <div className="mt-8 p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
                  <p className="text-green-800 dark:text-green-200 font-semibold">
                    ✅ Campaign Created Successfully!
                  </p>
                  <p className="text-sm text-green-700 dark:text-green-300 mt-1">
                    Processing time: {campaignData.processing_time?.toFixed(2) || '0.00'}s
                    {campaignData.transcript && ` | Transcript: ${campaignData.transcript.length} chars`}
                  </p>
                  {campaignData.strategy?.key_themes && (
                    <p className="text-sm text-green-700 dark:text-green-300">
                      Themes: {campaignData.strategy.key_themes.join(", ")}
                    </p>
                  )}
                </div>
                
                <CampaignResults data={campaignData} />
                <ExportManager campaignData={campaignData} />
              </>
            )}

            {/* Debug Info - Shows in development */}
            {process.env.NODE_ENV === 'development' && campaignData && (
              <details className="mt-4 p-4 bg-gray-100 dark:bg-gray-800 rounded">
                <summary className="cursor-pointer text-sm font-mono">Debug: Campaign Data</summary>
                <pre className="mt-2 text-xs overflow-auto max-h-96">
                  {JSON.stringify(campaignData, null, 2)}
                </pre>
              </details>
            )}
            
            {/* Debug Info for empty states */}
            {process.env.NODE_ENV === 'development' && !campaignData && orchStatus === 'completed' && (
              <div className="mt-4 p-4 bg-red-100 dark:bg-red-900/20 rounded">
                <p className="text-red-800 dark:text-red-200">
                  ⚠️ Campaign completed but no data received. Check console for errors.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}