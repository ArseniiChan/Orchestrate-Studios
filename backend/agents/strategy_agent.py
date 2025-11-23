"""
Strategy Intelligence Agent - FIXED VERSION
Analyzes video transcript to generate marketing strategy
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

async def analyze_transcript(transcript: str) -> Dict[str, Any]:
    """
    Analyze video transcript to create marketing strategy
    FIXED: Now actually uses the transcript content
    """
    try:
        # CRITICAL FIX: Validate and use the actual transcript
        if not transcript or len(transcript.strip()) < 10:
            logger.warning(f"Invalid transcript: '{transcript[:50] if transcript else 'None'}'")
            transcript = "Product or service video content"
        
        logger.info(f"Analyzing transcript ({len(transcript)} chars): {transcript[:200]}...")
        
        # Parse transcript to extract themes
        transcript_lower = transcript.lower()
        
        # Extract key themes from the ACTUAL transcript
        themes = []
        
        # Check for common topics in the transcript
        topic_keywords = {
            "AI and Technology": ["ai", "artificial intelligence", "machine learning", "technology", "software", "app"],
            "Marketing and Business": ["marketing", "business", "sales", "revenue", "growth", "customers"],
            "Health and Fitness": ["fitness", "health", "workout", "exercise", "nutrition", "wellness"],
            "Education": ["learn", "education", "course", "tutorial", "training", "students"],
            "Product Launch": ["launch", "introducing", "new", "revolutionary", "innovative"],
            "Social Media": ["tiktok", "instagram", "youtube", "content", "viral", "followers"],
        }
        
        for theme, keywords in topic_keywords.items():
            if any(keyword in transcript_lower for keyword in keywords):
                themes.append(theme)
        
        # If no themes found, extract from first part of transcript
        if not themes:
            first_words = transcript[:100].replace('\n', ' ').strip()
            themes.append(f"Topic: {first_words[:50]}...")
        
        # Determine target audience based on transcript content
        target_audience = "General audience"
        
        if any(word in transcript_lower for word in ["enterprise", "business", "company", "corporate"]):
            target_audience = "Business professionals and decision makers"
        elif any(word in transcript_lower for word in ["developer", "coding", "programming", "api"]):
            target_audience = "Developers and technical professionals"
        elif any(word in transcript_lower for word in ["fitness", "health", "workout", "diet"]):
            target_audience = "Health-conscious individuals and fitness enthusiasts"
        elif any(word in transcript_lower for word in ["student", "learn", "education", "course"]):
            target_audience = "Students and lifelong learners"
        elif any(word in transcript_lower for word in ["entrepreneur", "startup", "founder"]):
            target_audience = "Entrepreneurs and startup founders"
        
        # Extract value proposition from transcript
        value_prop = transcript[:150].replace('\n', ' ').strip()
        if len(value_prop) > 150:
            value_prop = value_prop[:147] + "..."
        
        # Build strategy using ACTUAL transcript content
        strategy = {
            "analysis_source": "video_transcript",
            "transcript_analyzed": True,
            "transcript_length": len(transcript),
            "target_audience": f"{target_audience} interested in: {themes[0] if themes else 'content'}",
            "primary_demographic": target_audience,
            "psychographics": [
                "Early adopters of new solutions",
                "Value efficiency and innovation",
                "Seek proven results"
            ],
            "key_themes": themes[:3],  # Top 3 themes from transcript
            "campaign_objectives": [
                f"Promote: {value_prop[:75]}",
                "Build brand awareness and engagement",
                "Generate qualified leads",
                "Drive conversions"
            ],
            "value_proposition": value_prop,
            "competitive_advantage": f"Unique approach: {transcript[:100]}",
            "content_pillars": [
                f"Pillar 1: {themes[0] if themes else 'Main Topic'}",
                f"Pillar 2: Behind-the-scenes",
                f"Pillar 3: Customer success stories"
            ],
            "messaging_tone": [
                "Professional yet approachable",
                "Data-driven and results-focused",
                "Inspiring and actionable"
            ],
            "success_metrics": {
                "engagement_rate": "25% target",
                "conversion_target": "5% of viewers",
                "reach_goal": "100K impressions in 30 days",
                "share_rate": "10% organic sharing"
            }
        }
        
        logger.info(f"Strategy created with themes: {themes[:3]}")
        return strategy
        
    except Exception as e:
        logger.error(f"Strategy analysis error: {str(e)}", exc_info=True)
        return {
            "error": str(e),
            "analysis_source": "error",
            "target_audience": "Unable to analyze",
            "key_themes": ["Error in analysis"],
            "transcript_length": len(transcript) if transcript else 0
        }

# IBM Granite model integration (when ready)
async def call_granite_model(transcript: str) -> Dict[str, Any]:
    """
    Call IBM Granite model for enhanced analysis
    This would integrate with IBM watsonx.ai
    """
    # For now, use the local analysis
    return await analyze_transcript(transcript)

# Main entry point for the agent
async def execute(transcript: str) -> Dict[str, Any]:
    """
    Main execution function for Strategy Agent
    """
    logger.info("Strategy Agent executing...")
    result = await analyze_transcript(transcript)
    logger.info(f"Strategy Agent complete. Found {len(result.get('key_themes', []))} themes")
    return result