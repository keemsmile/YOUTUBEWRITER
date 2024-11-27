from .base_agent import BaseAgent
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage
from slugify import slugify
import json

class SEOAgent(BaseAgent):
    def __init__(self):
        super().__init__("seo_agent")
        self.llm = ChatOpenAI(temperature=0.7)

    def analyze(self, content):
        """Analyze content and generate SEO recommendations"""
        system_prompt = """You are an SEO expert. Analyze the content and provide SEO recommendations.
        Return your response in the following JSON format:
        {
            "title": "SEO optimized title",
            "meta_description": "Compelling meta description",
            "keywords": ["keyword1", "keyword2", "etc"],
            "tldr_points": ["point1", "point2", "etc"],
            "user_intent": ["search intent1", "search intent2", "etc"]
        }"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Analyze this content: {content}")
        ]

        try:
            # Get response from LLM
            result = self.llm.invoke(messages)
            
            # Parse the JSON response
            seo_data = json.loads(result.content)
            
            # Ensure all required fields exist
            seo_data = {
                "title": seo_data.get("title", ""),
                "meta_description": seo_data.get("meta_description", ""),
                "keywords": seo_data.get("keywords", []),
                "url_slug": slugify(seo_data.get("title", "")),
                "tldr_points": seo_data.get("tldr_points", []),
                "user_intent": seo_data.get("user_intent", [])
            }
            
            # Save the SEO data for debugging
            self.save_output(seo_data, "seo_analysis.json")
            
            return seo_data
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error processing LLM response: {e}")
            print(f"Raw response: {result.content}")
            # If JSON parsing fails, create a basic structure
            default_seo = {
                "title": "Article Title",
                "meta_description": "Article description",
                "keywords": ["article"],
                "url_slug": "article",
                "tldr_points": ["Key point from the content"],
                "user_intent": ["General information"]
            }
            self.save_output(default_seo, "seo_analysis.json")
            return default_seo

    def process(self, input_data):
        return self.analyze(input_data)
