"""
Platform Optimization Agent - IBM watsonx.ai Integration
Creates platform-specific content using IBM Granite models
"""

import os
import json
import logging
import httpx
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

class PlatformAgent:
    """
    Platform Optimization Agent with IBM watsonx.ai Integration
    """
    
    def __init__(self):
        self.name = "Platform Optimization Agent"
        self.watsonx_url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
        self.project_id = os.getenv("WATSONX_PROJECT_ID")
        self.api_key = os.getenv("IBM_CLOUD_API_KEY")
        self.model_id = "ibm/granite-13b-chat-v2"
        
    async def get_access_token(self) -> str:
        """Get IBM Cloud access token"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://iam.cloud.ibm.com/identity/token",
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    data={
                        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                        "apikey": self.api_key
                    }
                )
                if response.status_code == 200:
                    return response.json()["access_token"]
                else:
                    logger.error(f"Failed to get token: {response.text}")
                    return None
        except Exception as e:
            logger.error(f"Token error: {str(e)}")
            return None
    
    async def generate_tiktok_content_ai(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Generate TikTok content using IBM watsonx.ai"""
        try:
            token = await self.get_access_token()
            if not token:
                return None
            
            themes = strategy.get("key_themes", ["Content"])
            audience = strategy.get("target_audience", "General")
            value_prop = strategy.get("value_proposition", "")
            
            # Create prompt for TikTok content
            prompt = f"""Create viral TikTok content for this campaign:
Themes: {', '.join(themes[:3])}
Audience: {audience}
Value: {value_prop[:100]}

Generate:
1. Attention-grabbing hook (max 10 words)
2. Engaging caption (max 100 words)
3. 5 relevant hashtags
4. Video structure for 30 seconds

Format as JSON with keys: hook, caption, hashtags, structure"""
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
            
            body = {
                "input": prompt,
                "parameters": {
                    "decoding_method": "greedy",
                    "max_new_tokens": 300,
                    "min_new_tokens": 50,
                    "temperature": 0.7,
                    "top_p": 0.9
                },
                "model_id": self.model_id,
                "project_id": self.project_id
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.watsonx_url}/ml/v1/text/generation?version=2023-05-29",
                    headers=headers,
                    json=body
                )
                
                if response.status_code == 200:
                    result = response.json()
                    generated_text = result["results"][0]["generated_text"]
                    
                    # Parse AI response
                    try:
                        content = json.loads(generated_text)
                        return {
                            "ai_generated": True,
                            "hook": content.get("hook", f"🚀 {themes[0]} Revolution"),
                            "caption": content.get("caption", value_prop[:100]),
                            "hashtags": content.get("hashtags", ["#TikTok", "#Viral", "#ForYou"]),
                            "structure": content.get("structure", [])
                        }
                    except:
                        # Parse text response
                        lines = generated_text.split('\n')
                        return {
                            "ai_generated": True,
                            "hook": lines[0] if lines else f"🚀 {themes[0]}",
                            "caption": generated_text[:200],
                            "hashtags": ["#TikTok", "#Viral", "#AI", "#Innovation"],
                            "raw_ai_response": generated_text[:500]
                        }
                else:
                    logger.error(f"TikTok AI generation failed: {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.error(f"TikTok AI error: {str(e)}")
            return None
    
    async def generate_linkedin_content_ai(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Generate LinkedIn content using IBM watsonx.ai"""
        try:
            token = await self.get_access_token()
            if not token:
                return None
            
            themes = strategy.get("key_themes", ["Professional"])
            audience = strategy.get("target_audience", "Professionals")
            value_prop = strategy.get("value_proposition", "")
            
            prompt = f"""Create LinkedIn professional content:
Industry: {themes[0] if themes else 'Business'}
Audience: {audience}
Value: {value_prop[:100]}

Generate professional LinkedIn post with thought leadership tone.
Include: headline, opening, 3 key points, call-to-action."""
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
            
            body = {
                "input": prompt,
                "parameters": {
                    "decoding_method": "greedy",
                    "max_new_tokens": 250,
                    "temperature": 0.5,  # More conservative for LinkedIn
                    "top_p": 0.9
                },
                "model_id": self.model_id,
                "project_id": self.project_id
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.watsonx_url}/ml/v1/text/generation?version=2023-05-29",
                    headers=headers,
                    json=body
                )
                
                if response.status_code == 200:
                    result = response.json()
                    generated_text = result["results"][0]["generated_text"]
                    
                    return {
                        "ai_generated": True,
                        "platform": "LinkedIn",
                        "content": generated_text,
                        "headline": f"🎯 {themes[0]}: Transforming {audience}",
                        "hashtags": [f"#{t.replace(' ', '')}" for t in themes[:3]] + ["#Innovation", "#Leadership"]
                    }
                else:
                    return None
                    
        except Exception as e:
            logger.error(f"LinkedIn AI error: {str(e)}")
            return None
    
    async def execute(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate platform-optimized content using IBM watsonx.ai
        """
        try:
            logger.info(f"{self.name} optimizing with watsonx.ai...")
            
            # Extract strategy elements
            themes = strategy.get("key_themes", ["Content"])
            audience = strategy.get("target_audience", "General audience")
            value_prop = strategy.get("value_proposition", "Transform your business")
            
            # Try AI generation first
            tiktok_ai = None
            linkedin_ai = None
            
            if self.project_id and self.api_key:
                tiktok_ai = await self.generate_tiktok_content_ai(strategy)
                linkedin_ai = await self.generate_linkedin_content_ai(strategy)
            
            # Build TikTok content
            if tiktok_ai and tiktok_ai.get("ai_generated"):
                logger.info("✅ Using IBM watsonx.ai for TikTok content")
                tiktok_content = {
                    "source": "ibm_watsonx_ai",
                    "hook": tiktok_ai.get("hook", f"🚀 {themes[0]}"),
                    "caption": tiktok_ai.get("caption", value_prop[:150]),
                    "hashtags": tiktok_ai.get("hashtags", []),
                    "video_structure": {
                        "duration": "30-60 seconds",
                        "segments": tiktok_ai.get("structure", self._default_tiktok_structure(themes))
                    },
                    "optimization": {
                        "best_time": "6-9 PM local time",
                        "frequency": "3-5 times per week",
                        "engagement_tactics": ["Reply to comments", "Use trending sounds", "Create series"]
                    }
                }
            else:
                # Enhanced fallback
                logger.info("Using enhanced local TikTok generation")
                tiktok_content = self._generate_tiktok_local(themes, audience, value_prop)
            
            # Build LinkedIn content
            if linkedin_ai and linkedin_ai.get("ai_generated"):
                logger.info("✅ Using IBM watsonx.ai for LinkedIn content")
                linkedin_content = {
                    "source": "ibm_watsonx_ai",
                    "headline": linkedin_ai.get("headline"),
                    "content": linkedin_ai.get("content"),
                    "hashtags": linkedin_ai.get("hashtags"),
                    "format": "Native video with text post",
                    "best_practices": ["Post Tuesday-Thursday", "Include data points", "Ask questions"]
                }
            else:
                linkedin_content = self._generate_linkedin_local(themes, audience, value_prop)
            
            # YouTube Shorts (always local for now - can add AI later)
            youtube_content = self._generate_youtube_local(themes, value_prop)
            
            # Instagram Reels
            instagram_content = self._generate_instagram_local(themes, value_prop)
            
            return {
                "generation_timestamp": datetime.utcnow().isoformat(),
                "agent": self.name,
                "ai_powered": bool(tiktok_ai or linkedin_ai),
                "platforms_optimized": 4,
                "tiktok": tiktok_content,
                "linkedin": linkedin_content,
                "youtube_shorts": youtube_content,
                "instagram_reels": instagram_content,
                "cross_platform_strategy": {
                    "unified_message": value_prop[:100],
                    "content_pillars": themes[:3],
                    "posting_calendar": self._generate_calendar(),
                    "engagement_strategy": self._generate_engagement_strategy(audience)
                },
                "performance_indicators": {
                    "expected_reach": "100K+ across platforms",
                    "engagement_target": "7%+ average",
                    "conversion_goal": "2-3% CTR"
                }
            }
            
        except Exception as e:
            logger.error(f"Platform agent error: {str(e)}")
            return self._fallback_response(strategy)
    
    def _default_tiktok_structure(self, themes: List[str]) -> List[Dict[str, str]]:
        """Default TikTok video structure"""
        return [
            {"time": "0-3s", "content": "Hook - grab attention", "element": "Text overlay + visual"},
            {"time": "3-10s", "content": f"Problem - why {themes[0] if themes else 'this'} matters"},
            {"time": "10-20s", "content": "Solution - show the transformation"},
            {"time": "20-27s", "content": "Benefits - what viewers gain"},
            {"time": "27-30s", "content": "CTA - follow for more"}
        ]
    
    def _generate_tiktok_local(self, themes: List[str], audience: str, value_prop: str) -> Dict[str, Any]:
        """Local TikTok content generation"""
        main_theme = themes[0] if themes else "Innovation"
        
        # Create engaging hooks based on theme
        hooks = {
            "AI": f"🤖 AI just changed {audience.split()[0].lower()} forever",
            "Marketing": f"📱 Marketing hack that saves 3 hours daily",
            "Business": f"💼 How to 10x your business growth",
            "Technology": f"🚀 Tech that's transforming everything",
            "Default": f"🎯 {main_theme}: The game changer"
        }
        
        # Select appropriate hook
        hook = hooks.get(main_theme.split()[0], hooks["Default"])
        
        return {
            "source": "local_enhanced",
            "hook": hook,
            "caption": f"{value_prop[:100]}\n\n💡 Save this for later!\n\n#innovation #growth",
            "hashtags": [
                "#TikTok", "#ForYouPage", "#FYP",
                f"#{main_theme.replace(' ', '')}", 
                "#Viral", "#Trending", "#MustWatch"
            ],
            "video_structure": {
                "duration": "30-60 seconds",
                "segments": self._default_tiktok_structure(themes)
            },
            "visual_style": {
                "transitions": "Quick cuts every 3-4 seconds",
                "text": "Bold, animated text overlays",
                "music": "Trending audio or upbeat background"
            }
        }
    
    def _generate_linkedin_local(self, themes: List[str], audience: str, value_prop: str) -> Dict[str, Any]:
        """Local LinkedIn content generation"""
        return {
            "source": "local_enhanced",
            "headline": f"🎯 {themes[0] if themes else 'Innovation'} Insights for {audience}",
            "opening": f"{value_prop}\n\nHere's what forward-thinking professionals need to know:",
            "key_points": [
                f"→ {themes[0]}: The competitive advantage",
                f"→ Data-driven insights that matter",
                f"→ Actionable strategies for growth"
            ],
            "hashtags": [f"#{t.replace(' ', '')}" for t in themes[:3]] + ["#Leadership", "#Innovation"],
            "format": "Professional article or native video",
            "tone": "Thought leadership with data"
        }
    
    def _generate_youtube_local(self, themes: List[str], value_prop: str) -> Dict[str, Any]:
        """Local YouTube Shorts content generation"""
        return {
            "source": "local",
            "title": f"{themes[0] if themes else 'Amazing'} in 60 Seconds #Shorts",
            "description": f"{value_prop}\n\n⏱️ Timestamps:\n0:00 Intro\n0:15 Main Point\n0:45 Key Takeaway",
            "tags": [t.lower() for t in themes[:5]] + ["shorts", "viral", "trending"],
            "thumbnail_text": f"{themes[0] if themes else 'MUST SEE'}!",
            "structure": {
                "duration": "30-59 seconds",
                "format": "Vertical 9:16",
                "segments": [
                    "0-5s: Hook",
                    "5-40s: Value delivery",
                    "40-55s: Call to action"
                ]
            }
        }
    
    def _generate_instagram_local(self, themes: List[str], value_prop: str) -> Dict[str, Any]:
        """Local Instagram Reels content generation"""
        return {
            "source": "local",
            "caption": f"✨ {value_prop[:100]}\n\nSave this for later! 📌",
            "hashtags": [f"#{t.replace(' ', '').lower()}" for t in themes[:3]] + 
                      ["#reels", "#instagram", "#viral", "#trending"],
            "format": "9:16 vertical video",
            "features": ["Add to story", "Share to feed", "IGTV preview"],
            "engagement": "Ask question in caption for comments"
        }
    
    def _generate_calendar(self) -> Dict[str, str]:
        """Generate posting calendar"""
        return {
            "Monday": "Motivational content - Start strong",
            "Tuesday": "Educational tips - LinkedIn focus",
            "Wednesday": "Behind-the-scenes - Instagram/TikTok",
            "Thursday": "Tutorial/How-to - YouTube Shorts",
            "Friday": "Community engagement - All platforms",
            "Weekend": "Lighter content - Entertainment focus"
        }
    
    def _generate_engagement_strategy(self, audience: str) -> List[str]:
        """Generate engagement strategy based on audience"""
        strategies = [
            "Respond to all comments within 2 hours",
            "Create polls and questions to boost interaction",
            "Use trending sounds and hashtags",
            "Collaborate with micro-influencers",
            "Share user-generated content"
        ]
        
        if "business" in audience.lower() or "professional" in audience.lower():
            strategies.append("Share data-driven insights and case studies")
            strategies.append("Host LinkedIn Live sessions")
        else:
            strategies.append("Create challenge campaigns")
            strategies.append("Use interactive stickers and features")
        
        return strategies
    
    def _fallback_response(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback response if all fails"""
        themes = strategy.get("key_themes", ["Content"])
        return {
            "generation_timestamp": datetime.utcnow().isoformat(),
            "agent": self.name,
            "ai_powered": False,
            "platforms_optimized": 1,
            "tiktok": {
                "source": "fallback",
                "hook": f"Check out {themes[0] if themes else 'this'}!",
                "caption": "Follow for more content",
                "hashtags": ["#TikTok", "#Viral"]
            },
            "error": "Platform optimization limited - check configuration"
        }

# Module-level execute function
async def execute(strategy: Dict[str, Any]) -> Dict[str, Any]:
    """Execute platform optimization with IBM watsonx.ai"""
    agent = PlatformAgent()
    return await agent.execute(strategy)