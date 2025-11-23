"""
Platform Optimization Agent - FIXED VERSION
Creates platform-specific content based on strategy
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

async def create_tiktok_content(strategy: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create TikTok-optimized content from strategy
    FIXED: Uses actual strategy content, not generic
    """
    # Extract real content from strategy
    themes = strategy.get("key_themes", ["Content"])
    target = strategy.get("target_audience", "Everyone")
    value_prop = strategy.get("value_proposition", "Check this out")
    objectives = strategy.get("campaign_objectives", ["Learn more"])
    
    # Create hook based on ACTUAL themes
    main_theme = themes[0] if themes else "Amazing content"
    
    # Generate engaging hook from actual content
    if "AI" in main_theme or "Technology" in main_theme:
        hook = f"🤖 {value_prop[:60]}..."
    elif "Fitness" in main_theme or "Health" in main_theme:
        hook = f"💪 Transform your health: {value_prop[:50]}..."
    elif "Marketing" in main_theme or "Business" in main_theme:
        hook = f"📈 Grow your business: {value_prop[:50]}..."
    elif "Education" in main_theme:
        hook = f"🎓 Learn this now: {value_prop[:50]}..."
    else:
        hook = f"🚀 {main_theme}: {value_prop[:50]}..."
    
    # Create caption using ACTUAL strategy elements
    caption_parts = []
    
    # Add main message from objectives
    if objectives:
        caption_parts.append(objectives[0][:100])
    
    caption_parts.append("")  # Empty line
    caption_parts.append(f"Perfect for: {target[:80]}")
    caption_parts.append("")
    caption_parts.append("👇 Learn more in comments")
    
    # Generate relevant hashtags based on themes
    hashtags = []
    
    # Add theme-specific hashtags
    for theme in themes[:3]:
        hashtag = theme.replace(" ", "").replace("and", "")
        hashtags.append(f"#{hashtag}")
    
    # Add platform hashtags
    hashtags.extend([
        "#TikTok",
        "#ForYouPage",
        "#FYP",
        "#Viral",
        "#ContentCreator"
    ])
    
    # Limit to 10 hashtags (TikTok best practice)
    hashtags = hashtags[:10]
    
    return {
        "hook": hook[:100],  # TikTok hooks should be concise
        "caption": "\n".join(caption_parts),
        "hashtags": hashtags,
        "format": "15-30 second vertical video",
        "duration": "15-30 seconds",
        "cta": "Follow for more insights!",
        "posting_time": "6-9 PM local time (peak engagement)",
        "content_style": [
            "Fast-paced and engaging",
            "Text overlays for key points",
            "Trending audio if applicable"
        ],
        "visual_elements": [
            "Eye-catching thumbnail",
            "Captions for accessibility",
            "Dynamic transitions"
        ]
    }

async def create_instagram_content(strategy: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create Instagram Reels content from strategy
    """
    themes = strategy.get("key_themes", ["Content"])
    value_prop = strategy.get("value_proposition", "Amazing content")
    
    # Similar to TikTok but adjusted for Instagram
    return {
        "reel_hook": f"📸 {value_prop[:60]}",
        "caption": f"{value_prop}\n\n{themes[0] if themes else 'Check this out'}",
        "hashtags": [f"#{theme.replace(' ', '')}" for theme in themes[:5]] + ["#Reels", "#Instagram"],
        "format": "9:16 vertical video reel",
        "duration": "15-60 seconds"
    }

async def create_linkedin_content(strategy: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create LinkedIn content from strategy
    """
    themes = strategy.get("key_themes", ["Professional content"])
    value_prop = strategy.get("value_proposition", "Professional insights")
    target = strategy.get("primary_demographic", "Professionals")
    
    return {
        "headline": f"🎯 {themes[0] if themes else 'Industry Insights'}",
        "opening": value_prop[:200],
        "body": f"For {target}, this represents a significant opportunity...",
        "hashtags": [f"#{theme.replace(' ', '')}" for theme in themes[:3]] + ["#LinkedInLearning"],
        "format": "Native video or article",
        "tone": "Professional and thought-leadership focused"
    }

async def execute(strategy: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main execution function for Platform Agent
    FIXED: Creates content based on actual strategy
    """
    logger.info("Platform Agent executing...")
    logger.info(f"Creating content for themes: {strategy.get('key_themes', [])}")
    
    try:
        # Create platform-specific content
        tiktok = await create_tiktok_content(strategy)
        instagram = await create_instagram_content(strategy)
        linkedin = await create_linkedin_content(strategy)
        
        result = {
            "platforms_optimized": True,
            "content_created_from": "actual_strategy",
            "tiktok": tiktok,
            "instagram": instagram,
            "linkedin": linkedin,
            "strategy_themes_used": strategy.get("key_themes", []),
            "target_audience": strategy.get("target_audience", "General")
        }
        
        logger.info("Platform content created successfully")
        return result
        
    except Exception as e:
        logger.error(f"Platform Agent error: {str(e)}", exc_info=True)
        return {
            "platforms_optimized": False,
            "error": str(e),
            "tiktok": {"error": "Failed to create content"}
        }