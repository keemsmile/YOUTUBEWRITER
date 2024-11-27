from .base_agent import BaseAgent
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

class SocialMediaAgent(BaseAgent):
    def __init__(self):
        super().__init__("social_media_agent")
        self.llm = ChatOpenAI(temperature=0.7)

    def generate_posts(self, article, seo_data):
        """Generate social media posts for different platforms"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a social media marketing expert.
            Create engaging social media posts for the following platforms:
            - Twitter (X)
            - LinkedIn
            - Facebook
            - Instagram
            
            For each platform:
            1. Use appropriate tone and style
            2. Include relevant hashtags
            3. Optimize character count
            4. Include a compelling call-to-action
            5. Use the provided keywords when relevant
            
            Format the response as a JSON object with a key for each platform."""),
            ("user", """Article: {article}
            Keywords: {keywords}
            Title: {title}""")
        ])

        chain = prompt | self.llm
        posts = chain.invoke({
            "article": article,
            "keywords": ", ".join(seo_data["keywords"]),
            "title": seo_data["title"]
        })
        
        # Save the social media posts for debugging
        self.save_output(posts.content, "social_media_posts.json")
        
        return posts.content

    def process(self, input_data):
        article, seo_data = input_data
        return self.generate_posts(article, seo_data)
