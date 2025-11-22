"use client"

import { Download, Share2, AlertCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"

interface ExportManagerProps {
  campaignData: any
}

export function ExportManager({ campaignData }: ExportManagerProps) {
  const handleExportJSON = () => {
    const dataStr = JSON.stringify(campaignData, null, 2)
    const dataBlob = new Blob([dataStr], { type: "application/json" })
    const url = URL.createObjectURL(dataBlob)
    const link = document.createElement("a")
    link.href = url
    link.download = `campaign-${Date.now()}.json`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  const handleExportCSV = () => {
    const rows = [
      ["Field", "Value"],
      ["Primary Angle", campaignData.strategy.primary_angle],
      ["Target Audience", campaignData.strategy.target_audience],
      ["Key Messages", campaignData.strategy.key_messages.join("; ")],
      ["Content Pillars", campaignData.strategy.content_pillars.join("; ")],
      ["TikTok Hook", campaignData.tiktok.hook],
      ["Caption", campaignData.tiktok.caption],
      ["Hashtags", campaignData.tiktok.hashtags.join(", ")],
      ["Optimal Time", campaignData.tiktok.optimal_time],
    ]

    const csv = rows.map((row) => row.map((cell) => `"${String(cell).replace(/"/g, '""')}"`).join(",")).join("\n")

    const blob = new Blob([csv], { type: "text/csv" })
    const url = URL.createObjectURL(blob)
    const link = document.createElement("a")
    link.href = url
    link.download = `campaign-${Date.now()}.csv`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  const handleShareViaEmail = () => {
    const subject = "Marketing Campaign - AI Generated"
    const body = encodeURIComponent(
      `Check out this AI-generated marketing campaign!\n\n` +
        `Primary Angle: ${campaignData.strategy.primary_angle}\n` +
        `Target Audience: ${campaignData.strategy.target_audience}\n` +
        `TikTok Hook: ${campaignData.tiktok.hook}\n` +
        `Caption: ${campaignData.tiktok.caption}\n` +
        `Hashtags: ${campaignData.tiktok.hashtags.join(" ")}`,
    )
    window.open(`mailto:?subject=${subject}&body=${body}`)
  }

  return (
    <Card className="border border-border shadow-lg bg-gradient-to-br from-primary/5 to-blue-400/5">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Download className="w-5 h-5 text-primary" />
          Export Campaign
        </CardTitle>
        <CardDescription>Download and share your complete campaign package</CardDescription>
      </CardHeader>

      <CardContent className="space-y-4">
        <Alert>
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>
            Export your campaign in multiple formats for easy sharing and integration with your workflow
          </AlertDescription>
        </Alert>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          <Button
            onClick={handleExportJSON}
            variant="outline"
            className="flex items-center justify-center gap-2 h-12 hover:bg-primary hover:text-primary-foreground border-primary/20 transition-all bg-transparent"
          >
            <Download className="w-4 h-4" />
            <span>JSON</span>
          </Button>

          <Button
            onClick={handleExportCSV}
            variant="outline"
            className="flex items-center justify-center gap-2 h-12 hover:bg-primary hover:text-primary-foreground border-primary/20 transition-all bg-transparent"
          >
            <Download className="w-4 h-4" />
            <span>CSV</span>
          </Button>

          <Button
            onClick={handleShareViaEmail}
            variant="outline"
            className="flex items-center justify-center gap-2 h-12 hover:bg-primary hover:text-primary-foreground border-primary/20 transition-all sm:col-span-2 lg:col-span-1 bg-transparent"
          >
            <Share2 className="w-4 h-4" />
            <span>Email</span>
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
