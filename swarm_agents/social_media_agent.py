from .base_agent import BaseSwarmAgent
from typing import Dict, List, Any
import json
from pydantic import Field

class SocialMediaSwarmAgent(BaseSwarmAgent):
    platform_constraints: Dict[str, Dict[str, int]] = Field(
        default_factory=lambda: {
            "twitter": {"max_length": 280, "hashtag_limit": 3},
            "linkedin": {"max_length": 3000, "hashtag_limit": 5},
            "facebook": {"max_length": 5000, "hashtag_limit": 10}
        }
    )

    def __init__(self):
        instructions = """You are a social media expert agent responsible for creating engaging posts.
        Your goals are to:
        1. Create platform-specific content
        2. Use relevant hashtags
        3. Optimize post timing
        4. Follow platform constraints
        5. Drive engagement
        
        Always format your responses according to the function specifications."""

        super().__init__(
            name="social_media_agent",
            model="gpt-4",
            instructions=instructions,
            functions=[
                self.create_posts,
                self.generate_hashtags,
                self.optimize_post
            ],
            parallel_tool_calls=True
        )

    def create_posts(self, content: str, platform: str) -> List[Dict[str, Any]]:
        """Create platform-specific social media posts.
        
        Args:
            content: The source content
            platform: Target social media platform
            
        Returns:
            List of posts with content and metadata
        """
        return [{
            "content": "",
            "hashtags": [],
            "best_posting_time": "",
            "platform": platform
        }]

    def generate_hashtags(self, content: str, platform: str) -> List[str]:
        """Generate relevant hashtags for the content.
        
        Args:
            content: The post content
            platform: Target social media platform
            
        Returns:
            List of relevant hashtags
        """
        return []

    def optimize_post(self, post: Dict[str, Any], metrics: Dict[str, float]) -> Dict[str, Any]:
        """Optimize a post based on performance metrics.
        
        Args:
            post: The original post
            metrics: Performance metrics
            
        Returns:
            Optimized post
        """
        return {
            "content": "",
            "hashtags": [],
            "best_posting_time": "",
            "platform": post.get("platform", "")
        }

    async def generate_posts(self, content: str, platform: str) -> List[Dict[str, Any]]:
        """Generate social media posts for a specific platform"""
        try:
            constraints = self.platform_constraints.get(platform, {})
            
            # Use Swarm's function calling to create posts
            result = await self.execute(
                f"Please create social media posts for {platform} with these constraints:\n\nContent:\n{content}\n\nConstraints:\n{json.dumps(constraints, indent=2)}"
            )

            # Extract the function call results
            if result.messages and result.messages[0].tool_calls:
                tool_call = result.messages[0].tool_calls[0]
                posts = json.loads(tool_call.function.arguments)
            else:
                posts = [{
                    "content": "",
                    "hashtags": [],
                    "best_posting_time": "",
                    "platform": platform
                }]

            return posts

        except Exception as e:
            print(f"Error generating social media posts: {str(e)}")
            return [{
                "content": "",
                "hashtags": [],
                "best_posting_time": "",
                "platform": platform
            }]

    async def optimize_posts(self, posts: List[Dict[str, Any]], metrics: Dict[str, float]) -> List[Dict[str, Any]]:
        """Optimize posts based on performance metrics"""
        try:
            # Use Swarm's function calling to optimize posts
            result = await self.execute(
                f"Please optimize these posts based on the metrics:\n\nPosts:\n{json.dumps(posts, indent=2)}\n\nMetrics:\n{json.dumps(metrics, indent=2)}"
            )

            # Extract the function call results
            if result.messages and result.messages[0].tool_calls:
                tool_call = result.messages[0].tool_calls[0]
                optimized_posts = json.loads(tool_call.function.arguments)
            else:
                optimized_posts = posts

            return optimized_posts

        except Exception as e:
            print(f"Error optimizing posts: {str(e)}")
            return posts
