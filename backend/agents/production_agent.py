"""
Production Task Agent - FIXED VERSION
Creates actionable tasks based on platform content
"""

import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

async def create_production_tasks(platform_content: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Create production tasks based on platform-specific content
    FIXED: Creates tasks specific to actual content
    """
    tasks = []
    
    # Extract content details
    tiktok = platform_content.get("tiktok", {})
    instagram = platform_content.get("instagram", {})
    themes = platform_content.get("strategy_themes_used", ["Content"])
    target = platform_content.get("target_audience", "General audience")
    
    # Get specific content elements
    hook = tiktok.get("hook", "Create engaging hook")
    caption = tiktok.get("caption", "Write caption")
    hashtags = tiktok.get("hashtags", [])
    
    # Base date for task scheduling
    today = datetime.now()
    
    # Task 1: Pre-production
    tasks.append({
        "id": "PROD-001",
        "title": f"Pre-production: Script for '{hook[:50]}...'",
        "description": f"Prepare script and storyboard for video about: {themes[0] if themes else 'main topic'}",
        "priority": "HIGH",
        "assignee": "Content Team",
        "due_date": today.strftime("%Y-%m-%d"),
        "estimated_hours": 1.5,
        "status": "TODO",
        "deliverables": [
            "Video script with timestamps",
            "Shot list",
            "Props/equipment needed"
        ],
        "content_details": {
            "hook": hook,
            "main_theme": themes[0] if themes else "Content"
        }
    })
    
    # Task 2: Video Production
    tasks.append({
        "id": "PROD-002",
        "title": f"Film TikTok video: {themes[0] if themes else 'Content'}",
        "description": f"Record 15-30 second video with hook: '{hook[:60]}'",
        "priority": "HIGH",
        "assignee": "Video Production",
        "due_date": (today + timedelta(days=1)).strftime("%Y-%m-%d"),
        "estimated_hours": 2,
        "status": "TODO",
        "requirements": [
            "Film in vertical format (9:16)",
            "Ensure good lighting",
            "Record clear audio",
            f"Target audience: {target[:50]}"
        ]
    })
    
    # Task 3: Post-production
    tasks.append({
        "id": "PROD-003",
        "title": "Edit video with captions and effects",
        "description": f"Add text overlays, captions: '{caption[:100]}...', trending effects",
        "priority": "HIGH",
        "assignee": "Video Editor",
        "due_date": (today + timedelta(days=1)).strftime("%Y-%m-%d"),
        "estimated_hours": 1.5,
        "status": "TODO",
        "editing_requirements": [
            "Add captions for accessibility",
            "Include text overlays for key points",
            "Add trending music/sounds",
            "Color correction and grading"
        ],
        "hashtags_to_include": hashtags[:5]
    })
    
    # Task 4: Thumbnail and Graphics
    tasks.append({
        "id": "PROD-004",
        "title": f"Create thumbnail for: {themes[0] if themes else 'video'}",
        "description": "Design eye-catching thumbnail and cover image",
        "priority": "MEDIUM",
        "assignee": "Graphic Designer",
        "due_date": (today + timedelta(days=2)).strftime("%Y-%m-%d"),
        "estimated_hours": 1,
        "status": "TODO",
        "specifications": [
            "1080x1920px for TikTok",
            "Include hook text",
            "High contrast for mobile viewing"
        ]
    })
    
    # Task 5: Publishing
    tasks.append({
        "id": "PROD-005",
        "title": f"Publish to TikTok with hashtags: {', '.join(hashtags[:3])}...",
        "description": f"Schedule and publish video with optimized caption and {len(hashtags)} hashtags",
        "priority": "MEDIUM",
        "assignee": "Social Media Manager",
        "due_date": (today + timedelta(days=2)).strftime("%Y-%m-%d"),
        "estimated_hours": 0.5,
        "status": "TODO",
        "publishing_checklist": [
            "Upload video",
            "Add caption with CTA",
            f"Include all {len(hashtags)} hashtags",
            "Schedule for 6-9 PM",
            "Cross-post to Instagram Reels"
        ],
        "hashtags": hashtags
    })
    
    # Task 6: Engagement Management
    tasks.append({
        "id": "PROD-006",
        "title": "Monitor and respond to engagement",
        "description": f"Track performance and engage with comments on {themes[0] if themes else 'content'}",
        "priority": "LOW",
        "assignee": "Community Manager",
        "due_date": (today + timedelta(days=3)).strftime("%Y-%m-%d"),
        "estimated_hours": 2,
        "status": "TODO",
        "kpis_to_track": [
            "View count",
            "Engagement rate",
            "Share count",
            "Comment sentiment",
            "Follower growth"
        ]
    })
    
    # Task 7: Performance Analysis
    tasks.append({
        "id": "PROD-007",
        "title": "Analyze campaign performance",
        "description": f"Create performance report for {themes[0] if themes else 'campaign'}",
        "priority": "LOW",
        "assignee": "Analytics Team",
        "due_date": (today + timedelta(days=7)).strftime("%Y-%m-%d"),
        "estimated_hours": 1,
        "status": "TODO",
        "metrics": [
            "ROI calculation",
            "Engagement analytics",
            "Audience insights",
            "Content performance",
            "Recommendations for optimization"
        ]
    })
    
    return tasks

async def execute(platform_content: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Main execution function for Production Agent
    """
    logger.info("Production Agent executing...")
    
    try:
        tasks = await create_production_tasks(platform_content)
        logger.info(f"Created {len(tasks)} production tasks")
        
        # Add summary
        total_hours = sum(task.get("estimated_hours", 0) for task in tasks)
        high_priority = len([t for t in tasks if t.get("priority") == "HIGH"])
        
        logger.info(f"Task summary: {len(tasks)} tasks, {total_hours} hours, {high_priority} high priority")
        
        return tasks
        
    except Exception as e:
        logger.error(f"Production Agent error: {str(e)}", exc_info=True)
        return [{
            "id": "ERROR",
            "title": "Failed to create tasks",
            "error": str(e)
        }]