"""
Strategy Intelligence Agent - IBM watsonx.ai Integration
Analyzes video transcript using IBM Granite models
"""

import os
import json
import logging
import httpx
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

class StrategyAgent:
    """
    Strategy Intelligence Agent with IBM watsonx.ai Integration
    """
    
    def __init__(self):
        self.name = "Strategy Intelligence Agent"
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
    
    async def call_watsonx_ai(self, prompt: str) -> Dict[str, Any]:
        """Call IBM watsonx.ai Granite model"""
        try:
            # Get access token
            token = await self.get_access_token()
            if not token:
                logger.warning("No token, using fallback")
                return None
            
            # Prepare the request
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
            
            # Create the prompt for strategy analysis
            system_prompt = """You are a marketing strategy expert. Analyze the transcript and provide:
1. Key themes (3-5 main topics)
2. Target audience definition
3. Value proposition
4. Campaign objectives
5. Content pillars

Respond in JSON format."""
            
            body = {
                "input": f"{system_prompt}\n\nTranscript: {prompt[:2000]}",  # Limit for token size
                "parameters": {
                    "decoding_method": "greedy",
                    "max_new_tokens": 500,
                    "min_new_tokens": 100,
                    "stop_sequences": [],
                    "repetition_penalty": 1
                },
                "model_id": self.model_id,
                "project_id": self.project_id
            }
            
            # Make the API call
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.watsonx_url}/ml/v1/text/generation?version=2023-05-29",
                    headers=headers,
                    json=body
                )
                
                if response.status_code == 200:
                    result = response.json()
                    generated_text = result["results"][0]["generated_text"]
                    
                    # Try to parse as JSON, fallback to text analysis
                    try:
                        return json.loads(generated_text)
                    except:
                        return self._parse_text_response(generated_text)
                else:
                    logger.error(f"watsonx.ai error: {response.status_code} - {response.text}")
                    return None
                    
        except Exception as e:
            logger.error(f"watsonx.ai call failed: {str(e)}")
            return None
    
    def _parse_text_response(self, text: str) -> Dict[str, Any]:
        """Parse text response from AI into structured format"""
        # Extract information from text response
        themes = []
        lines = text.split('\n')
        
        for line in lines:
            if 'theme' in line.lower() or 'topic' in line.lower():
                # Extract themes from the line
                themes.append(line.strip())
        
        return {
            "ai_generated": True,
            "raw_response": text[:500],
            "extracted_themes": themes[:5] if themes else ["Marketing", "Content", "Strategy"]
        }
    
    async def execute(self, transcript: str) -> Dict[str, Any]:
        """
        Analyze transcript using IBM watsonx.ai
        Falls back to local analysis if API fails
        """
        try:
            logger.info(f"{self.name} analyzing with watsonx.ai...")
            
            # Validate transcript
            if not transcript or len(transcript.strip()) < 10:
                transcript = "Marketing video content about product launch"
            
            # Try IBM watsonx.ai first
            ai_result = None
            if self.project_id and self.api_key:
                ai_result = await self.call_watsonx_ai(transcript)
            
            if ai_result:
                # Use AI-generated insights
                logger.info("✅ Using IBM watsonx.ai analysis")
                
                # Structure the AI response
                return {
                    "analysis_source": "ibm_watsonx_ai",
                    "model_used": self.model_id,
                    "transcript_analyzed": True,
                    "transcript_length": len(transcript),
                    "ai_insights": ai_result,
                    "key_themes": ai_result.get("extracted_themes", self._extract_local_themes(transcript)),
                    "target_audience": ai_result.get("target_audience", self._identify_audience(transcript)),
                    "value_proposition": ai_result.get("value_proposition", transcript[:150]),
                    "campaign_objectives": [
                        "Build brand awareness through AI-powered insights",
                        "Drive engagement with targeted content",
                        "Generate qualified leads",
                        "Establish thought leadership"
                    ],
                    "content_pillars": [
                        "Educational content",
                        "Product demonstrations",
                        "Customer success stories",
                        "Industry insights"
                    ],
                    "messaging_framework": {
                        "tone": "Professional yet approachable",
                        "key_messages": ai_result.get("key_messages", ["Innovation", "Efficiency", "Results"]),
                        "call_to_action": "Discover how we can transform your business"
                    }
                }
            else:
                # Fallback to enhanced local analysis
                logger.info("Using enhanced local analysis (watsonx.ai unavailable)")
                return await self._local_analysis(transcript)
                
        except Exception as e:
            logger.error(f"Strategy agent error: {str(e)}")
            return await self._local_analysis(transcript)
    
    def _extract_local_themes(self, transcript: str) -> List[str]:
        """Extract themes using local NLP-style analysis"""
        transcript_lower = transcript.lower()
        themes = []
        
        # Theme detection with keywords
        theme_patterns = {
            "AI and Automation": ["ai", "artificial intelligence", "automation", "machine learning", "automate"],
            "Digital Marketing": ["marketing", "campaign", "content", "social media", "brand"],
            "Business Growth": ["growth", "scale", "revenue", "roi", "performance"],
            "Customer Experience": ["customer", "user", "experience", "satisfaction", "engagement"],
            "Innovation": ["innovative", "transform", "revolutionize", "disrupt", "cutting-edge"],
            "Productivity": ["efficiency", "productivity", "streamline", "optimize", "workflow"],
            "Technology": ["technology", "platform", "software", "digital", "solution"],
            "Data Analytics": ["analytics", "data", "insights", "metrics", "measure"]
        }
        
        # Score each theme
        theme_scores = {}
        for theme, keywords in theme_patterns.items():
            score = sum(1 for keyword in keywords if keyword in transcript_lower)
            if score > 0:
                theme_scores[theme] = score
        
        # Sort themes by score
        sorted_themes = sorted(theme_scores.items(), key=lambda x: x[1], reverse=True)
        themes = [theme for theme, score in sorted_themes[:5]]
        
        # Ensure we have at least 3 themes
        if len(themes) < 3:
            themes.extend(["Content Strategy", "Digital Transformation", "Market Leadership"])
        
        return themes[:5]
    
    def _identify_audience(self, transcript: str) -> str:
        """Identify target audience from transcript"""
        transcript_lower = transcript.lower()
        
        # Audience indicators
        if any(word in transcript_lower for word in ["enterprise", "corporate", "b2b", "organization"]):
            return "Enterprise decision makers and B2B professionals"
        elif any(word in transcript_lower for word in ["startup", "founder", "entrepreneur"]):
            return "Startup founders and entrepreneurs"
        elif any(word in transcript_lower for word in ["developer", "api", "technical", "code"]):
            return "Technical professionals and developers"
        elif any(word in transcript_lower for word in ["marketing", "marketer", "content creator"]):
            return "Marketing professionals and content creators"
        elif any(word in transcript_lower for word in ["small business", "smb", "local"]):
            return "Small and medium business owners"
        else:
            return "Digital-savvy professionals seeking innovation"
    
    async def _local_analysis(self, transcript: str) -> Dict[str, Any]:
        """Enhanced local analysis when AI is unavailable"""
        themes = self._extract_local_themes(transcript)
        audience = self._identify_audience(transcript)
        
        # Extract value proposition
        sentences = transcript.split('.')
        value_prop = sentences[0][:150] if sentences else transcript[:150]
        
        return {
            "analysis_source": "local_enhanced",
            "transcript_analyzed": True,
            "transcript_length": len(transcript),
            "key_themes": themes,
            "target_audience": audience,
            "value_proposition": value_prop,
            "campaign_objectives": [
                f"Promote {themes[0] if themes else 'innovation'}",
                "Build brand awareness",
                "Drive qualified engagement",
                "Generate measurable ROI"
            ],
            "content_pillars": [
                f"{themes[0]} insights" if themes else "Industry insights",
                "Best practices and tutorials",
                "Success stories and case studies",
                "Thought leadership content"
            ],
            "messaging_framework": {
                "tone": "Professional and engaging",
                "key_messages": themes[:3],
                "call_to_action": "Transform your approach today"
            },
            "competitive_advantages": [
                "AI-powered insights",
                "Data-driven strategy",
                "Proven methodology"
            ],
            "success_metrics": {
                "awareness": "Reach 100K+ targeted impressions",
                "engagement": "Achieve 7%+ engagement rate",
                "conversion": "Generate 50+ qualified leads",
                "roi": "Deliver 300%+ return on investment"
            }
        }

# Module-level execute function for backward compatibility
async def execute(transcript: str) -> Dict[str, Any]:
    """Execute strategy analysis with IBM watsonx.ai"""
    agent = StrategyAgent()
    return await agent.execute(transcript)