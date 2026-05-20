import httpx
import json
import config
from typing import List, Dict, AsyncGenerator


class LLMClient:
    def __init__(self):
        self.base_url = config.OLLAMA_BASE_URL
        self.model = config.LLM_MODEL
        self.timeout = 120.0

    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2048,
        stream: bool = False,
    ) -> str:
        """Send a chat request to Ollama."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": stream,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens,
                    },
                },
            )
            response.raise_for_status()

            if stream:
                return response
            else:
                result = response.json()
                return result["message"]["content"]

    async def chat_stream(
        self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 2048
    ) -> AsyncGenerator[str, None]:
        """Stream chat responses from Ollama."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": True,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens,
                    },
                },
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            if "message" in data and "content" in data["message"]:
                                yield data["message"]["content"]
                        except json.JSONDecodeError:
                            continue

    async def generate(
        self, prompt: str, temperature: float = 0.7, max_tokens: int = 2048
    ) -> str:
        """Simple text generation."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens,
                    },
                },
            )
            response.raise_for_status()
            return response.json()["response"]


# Singleton instance
llm_client = LLMClient()
