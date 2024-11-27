from swarm.core import Swarm
from swarm.types import Result
from typing import Dict, List, Any
from .seo_agent import SEOSwarmAgent
from .journalist_agent import JournalistSwarmAgent
from .social_media_agent import SocialMediaSwarmAgent
import json

class ContentOrchestrator:
    def __init__(self):
        self.swarm = Swarm()
        self.seo_agent = SEOSwarmAgent()
        self.journalist_agent = JournalistSwarmAgent()
        self.social_media_agent = SocialMediaSwarmAgent()

        # No need to register agents with Swarm - they're used directly

    async def process_transcript(self, transcript: str) -> Dict:
        """Process a YouTube transcript through the agent pipeline"""
        try:
            # Step 1: SEO Analysis
            seo_result = await self.seo_agent.analyze(transcript)

            # Step 2: Article Writing
            article_result = await self.journalist_agent.write(transcript, seo_result)

            # Step 3: Social Media Posts
            social_posts = {}
            for platform in ["twitter", "linkedin", "facebook"]:
                posts = await self.social_media_agent.generate_posts(article_result["content"], platform)
                social_posts[platform] = posts

            return {
                "seo_analysis": seo_result,
                "article": article_result,
                "social_media_posts": social_posts,
                "success": True
            }

        except Exception as e:
            print(f"Error in content pipeline: {str(e)}")
            return {
                "error": str(e),
                "success": False
            }

    async def regenerate_article(self, transcript: str, feedback: str) -> str:
        """Regenerate the article based on feedback"""
        try:
            # Get current article
            current_article = await self.journalist_agent.write(transcript, {})
            
            # Revise based on feedback
            revised_article = await self.journalist_agent.revise(current_article["content"], feedback)
            
            return revised_article

        except Exception as e:
            print(f"Error regenerating article: {str(e)}")
            return ""

    async def optimize_social_posts(self, article: str, platform: str, metrics: Dict[str, float]) -> List[Dict[str, Any]]:
        """Optimize social media posts based on performance metrics"""
        try:
            # Generate initial posts
            posts = await self.social_media_agent.generate_posts(article, platform)
            
            # Optimize based on metrics
            optimized_posts = await self.social_media_agent.optimize_posts(posts, metrics)
            
            return optimized_posts

        except Exception as e:
            print(f"Error optimizing social posts: {str(e)}")
            return []
