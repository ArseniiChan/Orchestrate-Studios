"use client"

import type React from "react"

import { useState } from "react"
import { Menu, X, FileVideo, BarChart3, Settings } from "lucide-react"
import { Button } from "@/components/ui/button"

export function DashboardLayout({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setIsSidebarOpen] = useState(true)

  return (
    <div className="flex h-screen bg-background flex-col md:flex-row">
      {/* Mobile Menu Overlay */}
      {sidebarOpen && (
        <div className="fixed inset-0 z-40 bg-black/50 md:hidden" onClick={() => setIsSidebarOpen(false)} />
      )}

      {/* Sidebar */}
      <div
        className={`fixed md:relative left-0 top-0 z-50 h-screen bg-sidebar border-r border-sidebar-border transition-all duration-300 ease-in-out w-64 ${
          !sidebarOpen && "-translate-x-full md:translate-x-0"
        }`}
      >
        <div className="flex flex-col h-full overflow-hidden">
          {/* Logo */}
          <div className="px-6 py-6 border-b border-sidebar-border flex-shrink-0">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-sidebar-primary flex items-center justify-center flex-shrink-0">
                <FileVideo className="w-5 h-5 text-sidebar-primary-foreground" />
              </div>
              <h1 className="text-lg font-bold text-sidebar-foreground hidden sm:block">MarketOps</h1>
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
            <SidebarItem icon={<FileVideo className="w-5 h-5" />} label="Campaigns" active />
            <SidebarItem icon={<BarChart3 className="w-5 h-5" />} label="Analytics" />
            <SidebarItem icon={<Settings className="w-5 h-5" />} label="Settings" />
          </nav>

          {/* Footer */}
          <div className="px-4 py-6 border-t border-sidebar-border flex-shrink-0">
            <div className="text-xs text-sidebar-foreground/60">
              <p className="font-semibold mb-1">AI Agents</p>
              <ul className="space-y-1">
                <li>• Strategy</li>
                <li>• Platform</li>
                <li>• Production</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Toggle Button */}
      <Button
        variant="ghost"
        size="icon"
        onClick={() => setIsSidebarOpen(!sidebarOpen)}
        className="fixed left-4 top-4 z-40 rounded-lg md:hidden"
        aria-label="Toggle sidebar"
      >
        {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
      </Button>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-y-auto w-full">{children}</div>
    </div>
  )
}

function SidebarItem({
  icon,
  label,
  active = false,
}: {
  icon: React.ReactNode
  label: string
  active?: boolean
}) {
  return (
    <button
      className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors focus-visible:outline-ring focus-visible:ring-2 ${
        active
          ? "bg-sidebar-primary text-sidebar-primary-foreground"
          : "text-sidebar-foreground/70 hover:bg-sidebar-accent text-sidebar-foreground/70"
      }`}
      aria-current={active ? "page" : undefined}
    >
      {icon}
      <span className="text-sm font-medium">{label}</span>
    </button>
  )
}
