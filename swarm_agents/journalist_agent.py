from .base_agent import BaseSwarmAgent
from typing import Dict, List, Any
import json

class JournalistSwarmAgent(BaseSwarmAgent):
    def __init__(self):
        instructions = """You are a journalist agent responsible for writing engaging articles.
        Your goals are to:
        1. Write clear and engaging articles
        2. Extract and use relevant quotes
        3. Structure content effectively
        4. Follow SEO recommendations
        5. Maintain journalistic integrity
        
        Always format your responses according to the function specifications."""

        super().__init__(
            name="journalist_agent",
            model="gpt-4",
            instructions=instructions,
            functions=[
                self.write_article,
                self.extract_quotes,
                self.structure_content
            ],
            parallel_tool_calls=True
        )

    def write_article(self, transcript: str, seo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Write an article based on the transcript and SEO recommendations.
        
        Args:
            transcript: The source transcript
            seo_data: SEO recommendations to follow
            
        Returns:
            Dict containing the article content and metadata
        """
        return {
            "title": "",
            "content": "",
            "sections": [],
            "quotes": []
        }

    def extract_quotes(self, transcript: str) -> List[str]:
        """Extract relevant quotes from the transcript.
        
        Args:
            transcript: The source transcript
            
        Returns:
            List of relevant quotes
        """
        return []

    def structure_content(self, content: str) -> Dict[str, Any]:
        """Structure the content into sections.
        
        Args:
            content: The content to structure
            
        Returns:
            Dict containing structured content
        """
        return {
            "introduction": "",
            "main_sections": [],
            "conclusion": ""
        }

    async def write(self, transcript: str, seo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Write an article based on transcript and SEO data"""
        try:
            # Use Swarm's function calling to write the article
            result = await self.execute(
                f"Please write an article based on this transcript and SEO data:\n\nTranscript:\n{transcript}\n\nSEO Data:\n{json.dumps(seo_data, indent=2)}"
            )

            # Extract the function call results
            if result.messages and result.messages[0].tool_calls:
                tool_call = result.messages[0].tool_calls[0]
                article_data = json.loads(tool_call.function.arguments)
            else:
                article_data = {
                    "title": "",
                    "content": "",
                    "sections": [],
                    "quotes": []
                }

            return article_data

        except Exception as e:
            print(f"Error in article writing: {str(e)}")
            return {
                "title": "",
                "content": "",
                "sections": [],
                "quotes": []
            }

    async def revise(self, content: str, feedback: str) -> str:
        """Revise content based on feedback"""
        try:
            # Use Swarm's function calling to revise the article
            result = await self.execute(
                f"Please revise this content based on the feedback:\n\nContent:\n{content}\n\nFeedback:\n{feedback}"
            )

            # Extract the function call results
            if result.messages and result.messages[0].tool_calls:
                tool_call = result.messages[0].tool_calls[0]
                revised_content = json.loads(tool_call.function.arguments)["content"]
            else:
                revised_content = content

            return revised_content

        except Exception as e:
            print(f"Error in content revision: {str(e)}")
            return content
