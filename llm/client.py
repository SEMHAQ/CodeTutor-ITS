"""
LLM Client for CodeTutor-ITS
Supports local HuggingFace models (Qwen2.5-7B-Instruct) via transformers.
"""

import asyncio
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import config
from typing import List, Dict


class LLMClient:
    """Local LLM client using transformers library."""

    def __init__(self):
        self.model_path = config.LLM_MODEL_PATH
        self.model_name = config.LLM_MODEL_NAME
        self.model = None
        self.tokenizer = None
        self._loaded = False

    def _load_model(self):
        """Load model and tokenizer (called once on first use)."""
        if self._loaded:
            return

        print(f"Loading model from {self.model_path}...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_path,
            trust_remote_code=True,
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True,
        )
        self._loaded = True
        print(f"Model {self.model_name} loaded successfully.")

    def _generate_sync(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        """Synchronous generation using transformers."""
        self._load_model()

        # Apply chat template
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        # Tokenize
        inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature if temperature > 0 else None,
                do_sample=temperature > 0,
                top_p=0.9 if temperature > 0 else None,
                repetition_penalty=1.1,
            )

        # Decode only the generated tokens
        generated_ids = outputs[0][inputs["input_ids"].shape[1]:]
        response = self.tokenizer.decode(generated_ids, skip_special_tokens=True)
        return response.strip()

    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2048,
        stream: bool = False,  # kept for API compatibility
    ) -> str:
        """Async wrapper for chat generation."""
        # Run synchronous generation in thread pool
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            self._generate_sync,
            messages,
            temperature,
            max_tokens,
        )
        return result

    async def generate(
        self, prompt: str, temperature: float = 0.7, max_tokens: int = 2048
    ) -> str:
        """Simple text generation (wraps prompt in chat format)."""
        messages = [{"role": "user", "content": prompt}]
        return await self.chat(messages, temperature, max_tokens)


# Singleton instance
llm_client = LLMClient()
