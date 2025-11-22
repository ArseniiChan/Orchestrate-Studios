"use client"

import { useState } from "react"
import { Target, Copy, Check } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"

interface StrategyCardProps {
  strategy: {
    primary_angle: string
    target_audience: string
    key_messages: string[]
    content_pillars: string[]
  }
}

export function StrategyCard({ strategy }: StrategyCardProps) {
  const [copied, setCopied] = useState(false)

  const handleCopy = async (text: string) => {
    await navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <Card className="border border-border shadow-lg h-full hover:shadow-xl transition-shadow">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Target className="w-5 h-5 text-primary" />
          Strategy
        </CardTitle>
        <CardDescription>Content positioning and audience insights</CardDescription>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Primary Angle */}
        <div className="space-y-2">
          <div className="flex items-start justify-between gap-2">
            <div className="flex-1">
              <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Primary Angle</p>
              <p className="text-sm font-medium text-foreground mt-1">{strategy.primary_angle}</p>
            </div>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => handleCopy(strategy.primary_angle)}
              className="flex-shrink-0 h-8 w-8"
            >
              {copied ? <Check className="w-4 h-4 text-green-600" /> : <Copy className="w-4 h-4" />}
            </Button>
          </div>
        </div>

        {/* Target Audience */}
        <div className="space-y-2 pt-2 border-t border-border">
          <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Target Audience</p>
          <p className="text-sm font-medium text-foreground">{strategy.target_audience}</p>
        </div>

        {/* Key Messages */}
        <div className="space-y-2 pt-2 border-t border-border">
          <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Key Messages</p>
          <div className="flex flex-wrap gap-2">
            {strategy.key_messages.map((msg) => (
              <Badge
                key={msg}
                variant="secondary"
                className="bg-primary/10 text-primary hover:bg-primary/20 cursor-pointer"
                onClick={() => handleCopy(msg)}
              >
                {msg}
              </Badge>
            ))}
          </div>
        </div>

        {/* Content Pillars */}
        <div className="space-y-2 pt-2 border-t border-border">
          <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Content Pillars</p>
          <div className="flex flex-wrap gap-2">
            {strategy.content_pillars.map((pillar) => (
              <Badge key={pillar} variant="outline" className="border-border text-foreground">
                {pillar}
              </Badge>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
