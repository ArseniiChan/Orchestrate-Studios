"""
IBM watsonx Orchestrate Agent Modules - AI-Powered Version
Complete integration with IBM watsonx.ai Granite models
"""

from .strategy_agent import StrategyAgent, execute as strategy_execute
from .platform_agent import PlatformAgent, execute as platform_execute  
from .production_agent import ProductionAgent, execute as production_execute
from .analytics_agent import AnalyticsAgent, execute as analytics_execute

# Create singleton instances
strategy_agent = StrategyAgent()
platform_agent = PlatformAgent()
production_agent = ProductionAgent()
analytics_agent = AnalyticsAgent()

__all__ = [
    'strategy_agent',
    'platform_agent',
    'production_agent',
    'analytics_agent',
    'StrategyAgent',
    'PlatformAgent',
    'ProductionAgent',
    'AnalyticsAgent',
    'strategy_execute',
    'platform_execute',
    'production_execute',
    'analytics_execute'
]

# Version info
__version__ = "2.0.0"
__ibm_integration__ = True
__model__ = "ibm/granite-13b-chat-v2"