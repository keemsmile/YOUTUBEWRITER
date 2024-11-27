from .base_agent import BaseAgent
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

class EditorAgent(BaseAgent):
    def __init__(self):
        super().__init__("editor_agent")
        self.llm = ChatOpenAI(temperature=0.3)  # Lower temperature for more consistent editing

    def edit(self, article):
        """Edit the article to meet New York Times standards"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a senior editor at The New York Times.
            Review and edit the article to ensure it meets the following criteria:
            1. Maintains The New York Times style and tone
            2. Has clear and concise language
            3. Uses proper grammar and punctuation
            4. Has a strong narrative flow
            5. Includes proper transitions between paragraphs
            6. Maintains journalistic integrity
            
            Return the edited article with improvements."""),
            ("user", "{article}")
        ])

        chain = prompt | self.llm
        edited = chain.invoke({"article": article})
        
        # Save the edited article for debugging
        self.save_output(edited.content, "edited_article.txt")
        
        return edited.content

    def process(self, input_data):
        return self.edit(input_data)
