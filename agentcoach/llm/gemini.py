import google.generativeai as genai
from agentcoach.llm.base import LLMAdapter, Message


class GeminiAdapter(LLMAdapter):
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    def generate(self, messages: list) -> str:
        system_parts = []
        contents = []
        for msg in messages:
            if msg.role == "system":
                system_parts.append(msg.content)
            elif msg.role == "user":
                contents.append({"role": "user", "parts": [msg.content]})
            elif msg.role == "assistant":
                contents.append({"role": "model", "parts": [msg.content]})

        if system_parts:
            self.model = genai.GenerativeModel(
                self.model.model_name,
                system_instruction="\n".join(system_parts),
            )

        response = self.model.generate_content(contents)
        return response.text
