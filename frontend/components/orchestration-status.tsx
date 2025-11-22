"use client"

import { useEffect, useState } from "react"
import { Zap, CheckCircle2, Clock, AlertCircle } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

interface Agent {
  name: string
  status: "pending" | "processing" | "completed" | "error"
  estimatedTime: string
  description: string
}

interface OrchestrationStatusProps {
  status: "idle" | "uploading" | "orchestrating" | "completed" | "error"
  onComplete: (data: any) => void
}

export function OrchestrationStatus({ status, onComplete }: OrchestrationStatusProps) {
  const [agents, setAgents] = useState<Agent[]>([
    {
      name: "Strategy Intelligence Agent",
      status: "pending",
      estimatedTime: "~45 sec",
      description: "Analyzing content angles and target audience",
    },
    {
      name: "Platform Optimization Agent",
      status: "pending",
      estimatedTime: "~35 sec",
      description: "Generating TikTok-optimized content",
    },
    {
      name: "Production Task Agent",
      status: "pending",
      estimatedTime: "~20 sec",
      description: "Creating production checklist",
    },
  ])

  useEffect(() => {
    if (status === "orchestrating") {
      runOrchestrationPipeline()
    }
  }, [status])

  const runOrchestrationPipeline = async () => {
    // Agent 1: Strategy
    setAgents((prev) => [{ ...prev[0], status: "processing" }, prev[1], prev[2]])
    await new Promise((resolve) => setTimeout(resolve, 2500))
    setAgents((prev) => [{ ...prev[0], status: "completed" }, prev[1], prev[2]])

    // Agent 2: Platform
    setAgents((prev) => [prev[0], { ...prev[1], status: "processing" }, prev[2]])
    await new Promise((resolve) => setTimeout(resolve, 2000))
    setAgents((prev) => [prev[0], { ...prev[1], status: "completed" }, prev[2]])

    // Agent 3: Production
    setAgents((prev) => [prev[0], prev[1], { ...prev[2], status: "processing" }])
    await new Promise((resolve) => setTimeout(resolve, 1500))
    setAgents((prev) => [prev[0], prev[1], { ...prev[2], status: "completed" }])

    // Emit completion with sample data
    await new Promise((resolve) => setTimeout(resolve, 500))
    onComplete(generateSampleCampaignData())
  }

  const generateSampleCampaignData = () => {
    return {
      strategy: {
        primary_angle: "Behind-the-scenes transformation story",
        target_audience: "Gen Z entrepreneurs (18-28)",
        key_messages: ["Innovation", "Authenticity", "Growth", "Community"],
        content_pillars: ["Education", "Entertainment", "Inspiration"],
      },
      tiktok: {
        hook: "You won't believe what this AI just created...",
        caption: "From idea to viral content in seconds ✨ #AI #ContentCreation #MarketingHacks",
        hashtags: ["#viral", "#ai", "#marketing", "#tiktok", "#contenttips", "#entrepreneurship"],
        optimal_time: "Tuesday 6-9 PM ET",
      },
      tasks: [
        { task: "Review generated hook text", priority: "HIGH", estimated_time: "5 min", completed: false },
        { task: "Film B-roll footage", priority: "HIGH", estimated_time: "30 min", completed: false },
        { task: "Add music and sound effects", priority: "MEDIUM", estimated_time: "15 min", completed: false },
        { task: "Schedule post for optimal time", priority: "MEDIUM", estimated_time: "5 min", completed: false },
        { task: "Prepare additional hashtag variations", priority: "LOW", estimated_time: "10 min", completed: false },
      ],
    }
  }

  return (
    <Card className="border border-border shadow-lg overflow-hidden">
      <CardHeader className="bg-primary/5 border-b border-border">
        <CardTitle className="flex items-center gap-2">
          <Zap className="w-5 h-5 text-primary" />
          AI Orchestration Pipeline
        </CardTitle>
        <CardDescription>Watch as our 3-agent workflow transforms your content</CardDescription>
      </CardHeader>

      <CardContent className="pt-6">
        <div className="space-y-4">
          {agents.map((agent, idx) => (
            <div key={idx} className="relative">
              {/* Connection Line */}
              {idx < agents.length - 1 && (
                <div className="absolute left-6 top-12 w-0.5 h-8 bg-gradient-to-b from-border to-transparent" />
              )}

              <div className="flex gap-4">
                {/* Status Icon */}
                <div className="flex-shrink-0">
                  <div
                    className={`w-12 h-12 rounded-lg flex items-center justify-center transition-all ${
                      agent.status === "completed"
                        ? "bg-green-500/10 text-green-600"
                        : agent.status === "processing"
                          ? "bg-primary/10 text-primary animate-pulse-soft"
                          : "bg-muted text-muted-foreground"
                    }`}
                  >
                    {agent.status === "completed" && <CheckCircle2 className="w-6 h-6" />}
                    {agent.status === "processing" && <Clock className="w-6 h-6 animate-spin" />}
                    {agent.status === "pending" && <Clock className="w-6 h-6" />}
                    {agent.status === "error" && <AlertCircle className="w-6 h-6" />}
                  </div>
                </div>

                {/* Content */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <h3 className="font-semibold text-foreground">{agent.name}</h3>
                      <p className="text-sm text-muted-foreground">{agent.description}</p>
                    </div>
                    <span className="text-xs px-2 py-1 rounded-md bg-muted text-muted-foreground whitespace-nowrap">
                      {agent.estimatedTime}
                    </span>
                  </div>

                  {/* Status Badge */}
                  <div className="mt-2">
                    <span
                      className={`text-xs font-medium px-2 py-1 rounded inline-block ${
                        agent.status === "completed"
                          ? "bg-green-500/10 text-green-700 dark:text-green-400"
                          : agent.status === "processing"
                            ? "bg-primary/10 text-primary"
                            : "bg-muted text-muted-foreground"
                      }`}
                    >
                      {agent.status.charAt(0).toUpperCase() + agent.status.slice(1)}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ))}

          {/* Overall Progress */}
          <div className="mt-6 pt-4 border-t border-border">
            <div className="flex justify-between text-sm mb-2">
              <span className="font-medium text-foreground">Overall Progress</span>
              <span className="text-muted-foreground">
                {agents.filter((a) => a.status === "completed").length} / {agents.length}
              </span>
            </div>
            <div className="w-full bg-border rounded-full h-2 overflow-hidden">
              <div
                className="bg-gradient-to-r from-primary to-blue-400 h-full transition-all duration-500"
                style={{
                  width: `${(agents.filter((a) => a.status === "completed").length / agents.length) * 100}%`,
                }}
              />
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
