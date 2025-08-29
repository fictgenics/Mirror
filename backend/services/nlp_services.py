# services/semantic_search.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class SemanticSearch:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.5-pro")

    async def expand_query(self, user_query: str) -> str:
        """
        Convert natural user query into GitHub-friendly keywords.
        """
        prompt = f"""
        Convert the following user request into optimized GitHub search keywords.
        Keep the output short, only space-separated keywords,
        no stopwords, no explanations.

        Example:
        User: show me repos about real-time chat apps with WebSockets
        Output: real-time chat websocket messaging socket.io

        User: show me repos where mcp is used to connect with notion
        Output: notion mcp integration connector server

        User: {user_query}
        Output:
        """

        response = self.model.generate_content(prompt)
        return response.text.strip()
