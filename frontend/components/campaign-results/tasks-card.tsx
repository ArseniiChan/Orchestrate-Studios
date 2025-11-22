"use client"

import { useState } from "react"
import { CheckSquare, Square, AlertCircle } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

interface Task {
  task: string
  priority: "HIGH" | "MEDIUM" | "LOW"
  estimated_time: string
  completed: boolean
}

interface TasksCardProps {
  tasks: Task[]
}

export function TasksCard({ tasks: initialTasks }: TasksCardProps) {
  const [tasks, setTasks] = useState(initialTasks)

  const toggleTask = (index: number) => {
    setTasks((prev) => prev.map((t, i) => (i === index ? { ...t, completed: !t.completed } : t)))
  }

  const completedCount = tasks.filter((t) => t.completed).length

  const priorityColors = {
    HIGH: "bg-red-500/10 text-red-700 dark:text-red-400",
    MEDIUM: "bg-yellow-500/10 text-yellow-700 dark:text-yellow-400",
    LOW: "bg-green-500/10 text-green-700 dark:text-green-400",
  }

  const priorityBorderColors = {
    HIGH: "border-red-500/20",
    MEDIUM: "border-yellow-500/20",
    LOW: "border-green-500/20",
  }

  return (
    <Card className="border border-border shadow-lg">
      <CardHeader className="bg-gradient-to-r from-primary/5 to-blue-400/5">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <CardTitle className="flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-primary" />
              Production Checklist
            </CardTitle>
            <CardDescription>Tasks to complete your campaign</CardDescription>
          </div>
          <div className="text-right">
            <p className="text-sm font-semibold text-foreground">
              {completedCount}/{tasks.length}
            </p>
            <p className="text-xs text-muted-foreground">Completed</p>
          </div>
        </div>
      </CardHeader>

      <CardContent className="pt-6">
        <div className="space-y-2">
          {tasks.map((task, idx) => (
            <button
              key={idx}
              onClick={() => toggleTask(idx)}
              className={`w-full flex items-start gap-3 p-3 rounded-lg border transition-colors ${
                task.completed ? "bg-green-500/5 border-green-500/20" : priorityBorderColors[task.priority]
              } hover:bg-card`}
            >
              {/* Checkbox */}
              <div className="flex-shrink-0 mt-0.5">
                {task.completed ? (
                  <CheckSquare className="w-5 h-5 text-green-600" />
                ) : (
                  <Square className="w-5 h-5 text-muted-foreground" />
                )}
              </div>

              {/* Content */}
              <div className="flex-1 text-left min-w-0">
                <p
                  className={`font-medium ${task.completed ? "line-through text-muted-foreground" : "text-foreground"}`}
                >
                  {task.task}
                </p>
                <p className="text-xs text-muted-foreground mt-1">Est. {task.estimated_time}</p>
              </div>

              {/* Priority Badge */}
              <div className="flex-shrink-0">
                <Badge className={`${priorityColors[task.priority]} border-0`}>{task.priority}</Badge>
              </div>
            </button>
          ))}
        </div>

        {/* Progress Bar */}
        <div className="mt-6 pt-4 border-t border-border">
          <div className="flex justify-between text-sm mb-2">
            <span className="font-medium text-foreground">Overall Progress</span>
            <span className="text-muted-foreground">{Math.round((completedCount / tasks.length) * 100)}%</span>
          </div>
          <div className="w-full bg-border rounded-full h-2 overflow-hidden">
            <div
              className="bg-gradient-to-r from-green-500 to-emerald-400 h-full transition-all duration-500"
              style={{ width: `${(completedCount / tasks.length) * 100}%` }}
            />
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
