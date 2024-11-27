from .base_agent import BaseAgent
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage

class JournalistAgent(BaseAgent):
    def __init__(self):
        super().__init__("journalist_agent")
        self.llm = ChatOpenAI(temperature=0.7)

    def write_article(self, transcript, seo_data):
        """Write an article based on the transcript and SEO recommendations"""
        # Format keywords and user intent
        keywords_str = ", ".join(seo_data["keywords"]) if isinstance(seo_data["keywords"], list) else seo_data["keywords"]
        user_intent_str = ", ".join(seo_data["user_intent"]) if isinstance(seo_data["user_intent"], list) else seo_data["user_intent"]

        system_prompt = f"""You are a professional journalist writing for The New York Times.
        Write an informative article based on the provided transcript and SEO requirements.
        
        Requirements:
        1. Use these keywords naturally: {keywords_str}
        2. Follow journalistic best practices and NYT style
        3. Make the content engaging and informative
        4. Include relevant quotes from the transcript
        5. Target this user intent: {user_intent_str}
        6. Keep the tone professional and authoritative
        
        Title: {seo_data["title"]}"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Write an article based on this transcript: {transcript}")
        ]

        # Generate the article
        article = self.llm.invoke(messages)

        # Save the article for debugging
        self.save_output(article.content, "article.txt")
        
        return article.content

    def process(self, input_data):
        transcript, seo_data = input_data
        return self.write_article(transcript, seo_data)
