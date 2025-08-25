import openai
import json
from config import settings

class QueryParser:
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def parse(self, query: str, context: dict) -> dict:
        """Uses an LLM to parse the user query into structured data."""
        prompt = f"""
        Parse the following user query and context into a structured JSON object.
        Identify key entities like 'product_category', 'target_audience', 'geography', and 'core_objective'.

        Query: "{query}"
        Context: {context}

        Respond ONLY with a JSON object.
        """
        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.0
        )
        return json.loads(response.choices[0].message.content)

    async def extract_keywords(self, text: str) -> list:
        """Extracts key search terms from a text string."""
        prompt = f"Extract the 3-5 most important keywords for a web search from this text: '{text}'. Respond with a JSON list of strings."
        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.0
        )
        # Assuming the response is a JSON object like {"keywords": ["term1", "term2"]}
        return json.loads(response.choices[0].message.content).get("keywords", [])
