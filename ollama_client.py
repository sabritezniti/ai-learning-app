"""
Ollama client for local LLM integration.
Provides a simple interface to interact with local models via Ollama.
"""

import requests
import json
import streamlit as st
from config import OLLAMA_BASE_URL, OLLAMA_MODEL


class OllamaClient:
    """Client for interacting with Ollama local LLM."""

    def __init__(self, model=None, base_url=None):
        self.model = model or OLLAMA_MODEL
        self.base_url = base_url or OLLAMA_BASE_URL
        self.is_available = self._check_availability()

    def _check_availability(self):
        """Check if Ollama service is running."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=3)
            return response.status_code == 200
        except:
            return False

    def get_available_models(self):
        """Get list of available models from Ollama."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [m["name"] for m in data.get("models", [])]
            return []
        except:
            return []

    def chat(self, messages, system_prompt=None, temperature=0.7, stream=True):
        """
        Send a chat completion request to Ollama.

        Args:
            messages: List of dicts with 'role' and 'content' keys
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            stream: Whether to stream the response

        Returns:
            Generator if stream=True, else full response string
        """
        if not self.is_available:
            return None

        payload = {
            "model": self.model,
            "messages": messages,
            "options": {
                "temperature": temperature,
            },
            "stream": stream
        }

        if system_prompt:
            payload["system"] = system_prompt

        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                stream=stream,
                timeout=120
            )

            if stream:
                return self._stream_response(response)
            else:
                return response.json().get("message", {}).get("content", "")

        except Exception as e:
            return f"Error: {str(e)}"

    def _stream_response(self, response):
        """Generator for streaming responses."""
        full_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode('utf-8'))
                    if "message" in data and "content" in data["message"]:
                        chunk = data["message"]["content"]
                        full_response += chunk
                        yield chunk
                    if data.get("done", False):
                        break
                except json.JSONDecodeError:
                    continue
        return full_response

    def generate(self, prompt, system_prompt=None, context=""):
        """
        Generate a response with context about a specific course.

        Args:
            prompt: User question
            system_prompt: System instructions
            context: Course context to include

        Returns:
            Response string
        """
        if not self.is_available:
            return None

        # Build system prompt with context
        full_system = system_prompt or """You are an expert AI tutor and mentor. You help students learn about Artificial Intelligence, Machine Learning, Deep Learning, and related topics. 

Be encouraging, clear, and pedagogical. Use examples when helpful. If the student asks about a specific course, refer to the course content provided in the context.

Respond in the same language as the user's question."""

        if context:
            full_system += f"\n\nCourse context: {context}"

        messages = [
            {"role": "system", "content": full_system},
            {"role": "user", "content": prompt}
        ]

        return self.chat(messages, stream=False)


def get_system_prompt(lang="fr"):
    """Get system prompt based on language."""
    prompts = {
        "fr": """Tu es un mentor IA expert en intelligence artificielle. Tu aides les étudiants à apprendre le Machine Learning, le Deep Learning, le NLP, la vision par ordinateur et l'apprentissage par renforcement.

Sois pédagogique, encourageant et clair. Utilise des exemples concrets quand c'est utile. Si l'étudiant pose une question sur un cours spécifique, réfère-toi au contenu du cours fourni dans le contexte.

Réponds toujours en français.""",

        "en": """You are an expert AI tutor specializing in Artificial Intelligence. You help students learn Machine Learning, Deep Learning, NLP, Computer Vision, and Reinforcement Learning.

Be pedagogical, encouraging, and clear. Use concrete examples when helpful. If the student asks about a specific course, refer to the course content provided in the context.

Always respond in English.""",

        "ar": """أنت مرشد ذكي متخصص في الذكاء الاصطناعي. تساعد الطلاب في تعلم التعلم الآلي، التعلم العميق، معالجة اللغات الطبيعية، رؤية الحاسوب، والتعلم المعزز.

كن تعليمياً، مشجعاً، وواضحاً. استخدم أمثلة ملموسة عندما يكون ذلك مفيداً. إذا سأل الطالب عن دورة محددة، راجع محتوى الدورة المقدم في السياق.

رد دائماً باللغة العربية."""
    }
    return prompts.get(lang, prompts["en"])


def initialize_mentor():
    """Initialize the Ollama mentor client."""
    if "mentor" not in st.session_state:
        st.session_state.mentor = OllamaClient()
    return st.session_state.mentor
