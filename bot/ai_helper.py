from openai import OpenAI
from django.conf import settings
import json

class AIChatBot:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # System prompt that defines RamBot's personality and knowledge
        self.system_prompt = """You are RamBot, an AI assistant specifically designed for Ramaiah Institute of Technology students. 
        You have extensive knowledge about:
        - Academic programs and courses
        - Campus facilities and locations
        - Student activities and clubs
        - College policies and procedures
        - Campus life and events
        
        Always provide accurate, helpful information specific to Ramaiah Institute of Technology. 
        If you're not sure about something specific to the college, acknowledge that and provide general guidance."""
    
    def get_response(self, user_message, conversation_history=None):
        try:
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history:
                    role = "assistant" if msg.is_bot else "user"
                    messages.append({"role": role, "content": msg.content})
            
            # Add the current user message
            messages.append({"role": "user", "content": user_message})
            
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7,
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"I apologize, but I encountered an error. Please try again later. Error: {str(e)}"
        