"use client"

import { StrategyCard } from "./campaign-results/strategy-card"
import { TiktokCard } from "./campaign-results/tiktok-card"
import { TasksCard } from "./campaign-results/tasks-card"

interface CampaignResultsProps {
  // ... keep your existing interface ...
}

// Replace this function:
export function CampaignResults({ data }: CampaignResultsProps) {
  // Map the data to what the child components expect
  const mappedData = {
    strategy: {
      ...data.strategy,
      primary_angle: data.strategy.key_themes?.[0] || "Marketing Strategy",
      key_messages: data.strategy.key_themes || [],
      goals: data.strategy.campaign_objectives || []
    },
    tiktok: {
      hook: data.platform_content?.tiktok?.hook || "",
      caption: data.platform_content?.tiktok?.caption || "",
      hashtags: data.platform_content?.tiktok?.hashtags || [],
      optimal_time: data.platform_content?.tiktok?.posting_time || "6-9 PM",
      format: data.platform_content?.tiktok?.format || "",
      duration: data.platform_content?.tiktok?.duration || "",
      cta: data.platform_content?.tiktok?.cta || ""
    },
    tasks: data.production_tasks?.tasks?.map(task => ({
      task: task.title || task.description || "",
      priority: task.priority || "MEDIUM",
      estimated_time: task.estimated_hours ? `${task.estimated_hours} hours` : "TBD",
      completed: task.status === "DONE"
    })) || []
  }

  console.log("Mapped TikTok data:", mappedData.tiktok);
  
  return (
    <div className="space-y-6 animate-slide-in">
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-2 text-pretty">Campaign Results</h2>
        <p className="text-muted-foreground">Your AI-generated marketing campaign is ready</p>
      </div>

      <div className="grid gap-6 grid-cols-1 lg:grid-cols-3">
        <div className="lg:col-span-1">
          <StrategyCard strategy={mappedData.strategy} />
        </div>
        <div className="lg:col-span-2">
          <TiktokCard tiktok={mappedData.tiktok} />
        </div>
      </div>

      <div>
        <TasksCard tasks={mappedData.tasks} />
      </div>
    </div>
  )
}