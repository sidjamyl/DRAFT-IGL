# src/llm/gemini_client.py

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


class GeminiClient:
    """
    Client très simple pour appeler un modèle Gemini.
    """

    def __init__(self, model_name: str = "gemini-2.0-flash-exp"):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY manquant dans le fichier .env")

        self.model_name = model_name
        self.client = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=api_key,
            temperature=0.7
        )

    def generate(self, prompt: str) -> str:
        """
        Envoie un prompt texte au modèle et renvoie la réponse texte.
        """
        response = self.client.invoke(prompt)
        return response.content
