"use client"

import { useState } from "react"
import { Music, Copy, Check, Download } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"

interface TiktokCardProps {
  tiktok: {
    hook: string
    caption: string
    hashtags: string[]
    optimal_time: string
  }
}

export function TiktokCard({ tiktok }: TiktokCardProps) {
  const [copiedSection, setCopiedSection] = useState<string | null>(null)

  const handleCopy = async (text: string, section: string) => {
    await navigator.clipboard.writeText(text)
    setCopiedSection(section)
    setTimeout(() => setCopiedSection(null), 2000)
  }

  const handleExportSection = () => {
    const tiktokData = {
      hook: tiktok.hook,
      caption: tiktok.caption,
      hashtags: tiktok.hashtags,
      optimal_time: tiktok.optimal_time,
      exported_at: new Date().toISOString(),
    }
    const dataStr = JSON.stringify(tiktokData, null, 2)
    const dataBlob = new Blob([dataStr], { type: "application/json" })
    const url = URL.createObjectURL(dataBlob)
    const link = document.createElement("a")
    link.href = url
    link.download = `tiktok-content-${Date.now()}.json`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  return (
    <Card className="border border-border shadow-lg hover:shadow-xl transition-shadow">
      <CardHeader className="bg-gradient-to-r from-primary/5 to-blue-400/5">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <CardTitle className="flex items-center gap-2">
              <Music className="w-5 h-5 text-primary" />
              TikTok Content
            </CardTitle>
            <CardDescription>Platform-optimized content ready to post</CardDescription>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={handleExportSection}
            className="flex items-center gap-2 bg-transparent"
          >
            <Download className="w-4 h-4" />
            Export
          </Button>
        </div>
      </CardHeader>

      <CardContent className="space-y-6 pt-6">
        {/* Hook Text */}
        <div className="space-y-2">
          <div className="flex items-start justify-between gap-2">
            <div className="flex-1">
              <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-1">Hook Text</p>
              <p className="text-base font-semibold text-foreground leading-relaxed">"{tiktok.hook}"</p>
            </div>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => handleCopy(tiktok.hook, "hook")}
              className="flex-shrink-0 h-8 w-8"
            >
              {copiedSection === "hook" ? <Check className="w-4 h-4 text-green-600" /> : <Copy className="w-4 h-4" />}
            </Button>
          </div>
        </div>

        {/* Caption */}
        <div className="space-y-2 pt-2 border-t border-border">
          <div className="flex items-start justify-between gap-2">
            <div className="flex-1">
              <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-1">Caption</p>
              <p className="text-sm text-foreground leading-relaxed">{tiktok.caption}</p>
            </div>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => handleCopy(tiktok.caption, "caption")}
              className="flex-shrink-0 h-8 w-8"
            >
              {copiedSection === "caption" ? (
                <Check className="w-4 h-4 text-green-600" />
              ) : (
                <Copy className="w-4 h-4" />
              )}
            </Button>
          </div>
        </div>

        {/* Hashtags */}
        <div className="space-y-2 pt-2 border-t border-border">
          <div className="flex items-start justify-between gap-2">
            <div className="flex-1">
              <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-2">
                Hashtag Suggestions
              </p>
              <div className="flex flex-wrap gap-2">
                {tiktok.hashtags.map((tag) => (
                  <Badge
                    key={tag}
                    className="bg-primary text-primary-foreground cursor-pointer hover:bg-primary/90"
                    onClick={() => handleCopy(tag, "hashtag")}
                  >
                    {tag}
                  </Badge>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Optimal Posting Time */}
        <div className="space-y-2 pt-2 border-t border-border">
          <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Optimal Posting Time</p>
          <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-primary/5 border border-primary/20">
            <div className="w-2 h-2 rounded-full bg-primary animate-pulse" />
            <span className="text-sm font-medium text-foreground">{tiktok.optimal_time}</span>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
