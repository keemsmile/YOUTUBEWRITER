from .base_agent import BaseSwarmAgent
from typing import List, Dict, Any
import json

class SEOSwarmAgent(BaseSwarmAgent):
    def __init__(self):
        instructions = """You are an SEO expert agent responsible for analyzing content and providing SEO recommendations.
        Your goals are to:
        1. Analyze content for key themes and topics
        2. Generate relevant keywords and phrases
        3. Create compelling meta descriptions
        4. Identify user intent
        5. Provide a clear content structure
        
        Always format your responses according to the function specifications."""

        super().__init__(
            name="seo_agent",
            model="gpt-4",
            instructions=instructions,
            functions=[
                self.analyze_content,
                self.generate_keywords,
                self.create_meta_description
            ],
            parallel_tool_calls=True
        )

    def analyze_content(self, content: str) -> Dict[str, Any]:
        """Analyze content and provide SEO recommendations.
        
        Args:
            content: The content to analyze
            
        Returns:
            Dict containing SEO analysis including title, meta description, keywords, etc.
        """
        return {
            "title": "",
            "meta_description": "",
            "keywords": [],
            "tldr_points": [],
            "user_intent": []
        }

    def generate_keywords(self, content: str) -> List[str]:
        """Generate relevant keywords from content.
        
        Args:
            content: The content to analyze
            
        Returns:
            List of relevant keywords
        """
        return []

    def create_meta_description(self, content: str) -> str:
        """Create a compelling meta description.
        
        Args:
            content: The content to summarize
            
        Returns:
            SEO-optimized meta description
        """
        return ""

    async def analyze(self, content: str) -> Dict[str, Any]:
        """Analyze content and return comprehensive SEO data"""
        try:
            # Use Swarm's function calling to get analysis
            result = await self.execute(
                f"Please analyze this content for SEO optimization:\n\n{content}"
            )

            # Extract the function call results
            if result.messages and result.messages[0].tool_calls:
                tool_call = result.messages[0].tool_calls[0]
                seo_data = json.loads(tool_call.function.arguments)
            else:
                seo_data = {
                    "title": "",
                    "meta_description": "",
                    "keywords": [],
                    "tldr_points": [],
                    "user_intent": []
                }

            return seo_data

        except Exception as e:
            print(f"Error in SEO analysis: {str(e)}")
            return {
                "title": "",
                "meta_description": "",
                "keywords": [],
                "tldr_points": [],
                "user_intent": []
            }

    async def optimize(self, content: str, target_keywords: List[str]) -> Dict[str, Any]:
        """Optimize content for given keywords"""
        try:
            optimization_prompt = f"""Please optimize this content for the following keywords: {', '.join(target_keywords)}

            Content:
            {content}

            Provide specific recommendations for optimization."""

            result = await self.execute(optimization_prompt)
            
            # Save optimization results
            optimization_data = {
                "original_content": content,
                "target_keywords": target_keywords,
                "recommendations": result.messages[0].content if result.messages else ""
            }
            self.save_output(optimization_data, "optimization.json")

            return optimization_data

        except Exception as e:
            print(f"Error in content optimization: {str(e)}")
            return {
                "error": str(e),
                "success": False
            }
