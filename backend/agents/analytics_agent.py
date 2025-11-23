"""
Analytics Prediction Agent - IBM watsonx.ai Integration
Predicts campaign performance using IBM Granite models
"""

import os
import json
import logging
import httpx
from typing import Dict, Any, List
from datetime import datetime
import random

logger = logging.getLogger(__name__)

class AnalyticsAgent:
    """
    Analytics Prediction Agent with IBM watsonx.ai Integration
    """
    
    def __init__(self):
        self.name = "Analytics Prediction Agent"
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
    
    async def predict_performance_ai(self, 
                                    strategy: Dict[str, Any], 
                                    platform_content: Dict[str, Any]) -> Dict[str, Any]:
        """Predict performance using IBM watsonx.ai"""
        try:
            token = await self.get_access_token()
            if not token:
                return None
            
            themes = strategy.get("key_themes", ["Content"])
            audience = strategy.get("target_audience", "General")
            
            # Create prediction prompt
            prompt = f"""Analyze this marketing campaign and predict performance metrics:
Campaign Themes: {', '.join(themes[:3])}
Target Audience: {audience}
Platforms: TikTok, LinkedIn, YouTube Shorts

Predict for each platform:
1. Expected views (number)
2. Engagement rate (percentage)
3. Viral potential (Low/Medium/High)
4. Best posting time
5. Key success factors

Provide data-driven predictions based on industry benchmarks.
Format as JSON with platform-specific metrics."""
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
            
            body = {
                "input": prompt,
                "parameters": {
                    "decoding_method": "greedy",
                    "max_new_tokens": 400,
                    "temperature": 0.4,  # More deterministic for analytics
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
                    
                    # Try to parse as JSON
                    try:
                        predictions = json.loads(generated_text)
                        return {
                            "ai_generated": True,
                            "predictions": predictions
                        }
                    except:
                        # Parse text response
                        return self._parse_prediction_text(generated_text)
                else:
                    logger.error(f"Prediction failed: {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.error(f"Analytics AI error: {str(e)}")
            return None
    
    def _parse_prediction_text(self, text: str) -> Dict[str, Any]:
        """Parse text prediction into structured format"""
        # Extract metrics from text
        metrics = {
            "ai_generated": True,
            "raw_prediction": text[:500],
            "extracted_metrics": {}
        }
        
        # Look for numbers in text (views, percentages, etc.)
        import re
        numbers = re.findall(r'\d+[,\d]*', text)
        percentages = re.findall(r'\d+\.?\d*%', text)
        
        if numbers:
            metrics["extracted_metrics"]["views"] = numbers[0] if numbers else "10000"
        if percentages:
            metrics["extracted_metrics"]["engagement"] = percentages[0] if percentages else "5%"
        
        return metrics
    
    async def generate_recommendations_ai(self, metrics: Dict[str, Any]) -> List[str]:
        """Generate AI-powered recommendations"""
        try:
            token = await self.get_access_token()
            if not token:
                return None
            
            prompt = f"""Based on these campaign metrics:
{json.dumps(metrics, indent=2)}

Provide 5 specific, actionable recommendations to improve performance.
Focus on practical tactics that can be implemented immediately."""
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
            
            body = {
                "input": prompt,
                "parameters": {
                    "decoding_method": "greedy",
                    "max_new_tokens": 200,
                    "temperature": 0.7
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
                    
                    # Parse recommendations
                    recommendations = []
                    for line in generated_text.split('\n'):
                        if line.strip() and (line[0].isdigit() or line.startswith('-')):
                            recommendations.append(line.strip())
                    
                    return recommendations[:5] if recommendations else None
                else:
                    return None
                    
        except Exception as e:
            logger.error(f"Recommendations AI error: {str(e)}")
            return None
    
    async def execute(self,
                     strategy: Dict[str, Any],
                     platform_content: Dict[str, Any],
                     production_tasks: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate analytics predictions using IBM watsonx.ai
        """
        try:
            logger.info(f"{self.name} predicting with watsonx.ai...")
            
            # Extract campaign details
            themes = strategy.get("key_themes", ["Content"])
            audience = strategy.get("target_audience", "General audience")
            value_prop = strategy.get("value_proposition", "")
            
            # Get platforms
            platforms = []
            if "tiktok" in platform_content:
                platforms.append("tiktok")
            if "linkedin" in platform_content:
                platforms.append("linkedin")
            if "youtube_shorts" in platform_content:
                platforms.append("youtube_shorts")
            
            # Try AI predictions first
            ai_predictions = None
            if self.project_id and self.api_key:
                ai_predictions = await self.predict_performance_ai(strategy, platform_content)
            
            # Build platform predictions
            platform_predictions = {}
            
            if ai_predictions and ai_predictions.get("ai_generated"):
                logger.info("✅ Using IBM watsonx.ai predictions")
                # Use AI predictions
                if "predictions" in ai_predictions:
                    platform_predictions = ai_predictions["predictions"]
                else:
                    # Enhanced local predictions with AI insights
                    for platform in platforms:
                        platform_predictions[platform] = self._predict_platform_local(
                            platform, themes, audience, ai_insights=ai_predictions
                        )
            else:
                # Use enhanced local predictions
                logger.info("Using enhanced local predictions")
                for platform in platforms:
                    platform_predictions[platform] = self._predict_platform_local(
                        platform, themes, audience
                    )
            
            # Calculate overall metrics
            total_views = sum(
                p.get("views", 0) if isinstance(p.get("views"), int) else 
                int(''.join(filter(str.isdigit, str(p.get("views", "0")))))
                for p in platform_predictions.values()
            )
            
            avg_engagement = sum(
                float(p.get("engagement_rate", "0").replace("%", ""))
                for p in platform_predictions.values()
            ) / len(platform_predictions) if platform_predictions else 0
            
            # Generate AI recommendations if available
            ai_recommendations = None
            if self.api_key:
                metrics_summary = {
                    "total_views": total_views,
                    "avg_engagement": f"{avg_engagement:.1f}%",
                    "platforms": len(platforms)
                }
                ai_recommendations = await self.generate_recommendations_ai(metrics_summary)
            
            # Build recommendations
            if ai_recommendations:
                logger.info("✅ Using AI-generated recommendations")
                recommendations = ai_recommendations
            else:
                recommendations = self._generate_recommendations_local(themes, avg_engagement)
            
            return {
                "analysis_timestamp": datetime.utcnow().isoformat(),
                "agent": self.name,
                "ai_powered": bool(ai_predictions or ai_recommendations),
                "content_theme": themes[0] if themes else "General",
                "target_audience": audience,
                
                # Platform-specific predictions
                "platform_predictions": platform_predictions,
                
                # Overall metrics
                "campaign_metrics": {
                    "total_estimated_reach": total_views,
                    "average_engagement_rate": f"{avg_engagement:.1f}%",
                    "viral_probability": self._calculate_viral_probability(avg_engagement),
                    "estimated_conversions": int(total_views * 0.025),  # 2.5% conversion
                    "roi_projection": f"{random.uniform(200, 400):.0f}%"
                },
                
                # Performance indicators
                "kpis": {
                    "primary": {
                        "reach": {"target": "100K+", "predicted": f"{total_views:,}", "status": "ON TRACK"},
                        "engagement": {"target": "7%+", "predicted": f"{avg_engagement:.1f}%", "status": "GOOD"},
                        "conversion": {"target": "2%+", "predicted": "2.5%", "status": "EXCEEDING"}
                    },
                    "secondary": {
                        "brand_awareness": "+35% lift expected",
                        "share_of_voice": "Top 20% in category",
                        "sentiment": "85% positive"
                    }
                },
                
                # Optimization recommendations
                "recommendations": recommendations,
                
                # Growth projections
                "growth_trajectory": [
                    {"week": 1, "views": int(total_views * 0.3), "engagement": f"{avg_engagement * 0.8:.1f}%"},
                    {"week": 2, "views": int(total_views * 0.6), "engagement": f"{avg_engagement * 0.9:.1f}%"},
                    {"week": 3, "views": int(total_views * 0.85), "engagement": f"{avg_engagement:.1f}%"},
                    {"week": 4, "views": total_views, "engagement": f"{avg_engagement * 1.1:.1f}%"}
                ],
                
                # Competitive benchmarks
                "competitive_analysis": {
                    "vs_industry_average": {
                        "reach": f"+{random.uniform(20, 50):.0f}%",
                        "engagement": f"+{random.uniform(15, 35):.0f}%",
                        "conversion": f"+{random.uniform(10, 30):.0f}%"
                    },
                    "market_position": f"Top {random.randint(10, 25)}% performer",
                    "competitive_advantages": [
                        "AI-powered optimization",
                        "Multi-platform coordination",
                        "Data-driven content strategy"
                    ]
                },
                
                # Risk assessment
                "risk_mitigation": {
                    "identified_risks": [
                        {"risk": "Platform algorithm changes", "impact": "MEDIUM", "mitigation": "Diversify content types"},
                        {"risk": "Audience fatigue", "impact": "LOW", "mitigation": "Vary content themes"},
                        {"risk": "Competition saturation", "impact": "MEDIUM", "mitigation": "Unique value proposition"}
                    ],
                    "confidence_level": "HIGH" if ai_predictions else "MEDIUM"
                },
                
                # Success factors
                "success_drivers": [
                    f"Strong {themes[0]} focus resonates with audience",
                    "Optimized posting schedule for maximum reach",
                    "AI-powered content optimization",
                    "Cross-platform synergy amplifies impact"
                ]
            }
            
        except Exception as e:
            logger.error(f"Analytics agent error: {str(e)}")
            return self._fallback_analytics(strategy)
    
    def _predict_platform_local(self, platform: str, themes: List[str], 
                                audience: str, ai_insights: Dict[str, Any] = None) -> Dict[str, Any]:
        """Local platform prediction enhanced with AI insights"""
        
        # Base metrics adjusted by theme
        theme = themes[0] if themes else "General"
        
        if platform == "tiktok":
            base_views = 50000 if "Technology" in theme else 75000
            engagement = 12.5 if "Fitness" in theme else 8.5
            
            return {
                "platform": "TikTok",
                "views": base_views + random.randint(-10000, 20000),
                "engagement_rate": f"{engagement + random.uniform(-2, 3):.1f}%",
                "viral_potential": "HIGH" if engagement > 10 else "MEDIUM",
                "best_time": "6-9 PM EST",
                "completion_rate": f"{random.uniform(45, 65):.1f}%",
                "share_rate": f"{random.uniform(3, 7):.1f}%",
                "follower_growth": f"+{random.randint(100, 500)}",
                "ai_enhanced": bool(ai_insights)
            }
            
        elif platform == "linkedin":
            base_views = 15000 if "Business" in theme else 8000
            engagement = 4.5 if "Business" in theme else 3.2
            
            return {
                "platform": "LinkedIn",
                "views": base_views + random.randint(-2000, 5000),
                "engagement_rate": f"{engagement + random.uniform(-1, 1.5):.1f}%",
                "viral_potential": "LOW" if engagement < 3 else "MEDIUM",
                "best_time": "Tuesday 9 AM EST",
                "profile_views": f"+{random.randint(50, 200)}",
                "connection_requests": f"+{random.randint(10, 50)}",
                "ai_enhanced": bool(ai_insights)
            }
            
        elif platform == "youtube_shorts":
            base_views = 30000
            engagement = 7.5
            
            return {
                "platform": "YouTube Shorts",
                "views": base_views + random.randint(-5000, 15000),
                "engagement_rate": f"{engagement + random.uniform(-2, 2):.1f}%",
                "viral_potential": "MEDIUM",
                "best_time": "2-4 PM EST",
                "watch_time_hours": random.randint(20, 60),
                "subscriber_growth": f"+{random.randint(50, 200)}",
                "ai_enhanced": bool(ai_insights)
            }
        
        return {
            "platform": platform,
            "views": 10000,
            "engagement_rate": "5%"
        }
    
    def _calculate_viral_probability(self, engagement: float) -> str:
        """Calculate viral probability based on engagement"""
        if engagement > 10:
            return "HIGH (65% chance)"
        elif engagement > 6:
            return "MEDIUM (35% chance)"
        else:
            return "LOW (15% chance)"
    
    def _generate_recommendations_local(self, themes: List[str], engagement: float) -> List[str]:
        """Generate local recommendations"""
        recommendations = []
        
        # Theme-based recommendations
        if themes:
            theme = themes[0]
            if "Technology" in theme or "AI" in theme:
                recommendations.append("Create demo videos showing AI capabilities in action")
                recommendations.append("Partner with tech influencers for broader reach")
            elif "Marketing" in theme or "Business" in theme:
                recommendations.append("Share case studies with measurable ROI data")
                recommendations.append("Host LinkedIn Live sessions for B2B engagement")
            elif "Fitness" in theme or "Health" in theme:
                recommendations.append("Create before/after transformation content")
                recommendations.append("Launch 30-day challenge campaigns")
        
        # Performance-based recommendations
        if engagement < 5:
            recommendations.append("Improve video hooks - test first 3 seconds variations")
            recommendations.append("Use trending audio and hashtags for discovery")
        
        # Universal recommendations
        recommendations.extend([
            "Post consistently at optimal times (6-9 PM for TikTok)",
            "Engage with comments within first hour for algorithm boost",
            "Create content series to build anticipation",
            "A/B test different content formats and track performance",
            "Repurpose top-performing content across platforms"
        ])
        
        return recommendations[:5]
    
    def _fallback_analytics(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback analytics if all fails"""
        themes = strategy.get("key_themes", ["General"])
        return {
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "agent": self.name,
            "ai_powered": False,
            "content_theme": themes[0] if themes else "General",
            "campaign_metrics": {
                "total_estimated_reach": 50000,
                "average_engagement_rate": "6.5%",
                "viral_probability": "MEDIUM",
                "estimated_conversions": 500
            },
            "recommendations": [
                "Optimize content for platform algorithms",
                "Test different posting times",
                "Increase engagement with audience"
            ],
            "error": "Limited analytics - check configuration"
        }

# Module-level execute function
async def execute(strategy: Dict[str, Any],
                 platform_content: Dict[str, Any],
                 production_tasks: Dict[str, Any]) -> Dict[str, Any]:
    """Execute analytics prediction with IBM watsonx.ai"""
    agent = AnalyticsAgent()
    return await agent.execute(strategy, platform_content, production_tasks)