"use client"

import { StrategyCard } from "./campaign-results/strategy-card"
import { TiktokCard } from "./campaign-results/tiktok-card"
import { TasksCard } from "./campaign-results/tasks-card"

interface CampaignResultsProps {
  data: {
    strategy: {
      primary_angle: string
      target_audience: string
      key_messages: string[]
      content_pillars: string[]
    }
    tiktok: {
      hook: string
      caption: string
      hashtags: string[]
      optimal_time: string
    }
    tasks: Array<{
      task: string
      priority: "HIGH" | "MEDIUM" | "LOW"
      estimated_time: string
      completed: boolean
    }>
  }
}

export function CampaignResults({ data }: CampaignResultsProps) {
  return (
    <div className="space-y-6 animate-slide-in">
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-2 text-pretty">Campaign Results</h2>
        <p className="text-muted-foreground">Your AI-generated marketing campaign is ready</p>
      </div>

      {/* Results Grid - Responsive */}
      <div className="grid gap-6 grid-cols-1 lg:grid-cols-3">
        <div className="lg:col-span-1">
          <StrategyCard strategy={data.strategy} />
        </div>
        <div className="lg:col-span-2">
          <TiktokCard tiktok={data.tiktok} />
        </div>
      </div>

      <div>
        <TasksCard tasks={data.tasks} />
      </div>
    </div>
  )
}
