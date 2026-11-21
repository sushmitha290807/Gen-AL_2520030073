import os
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass

import requests
from google import genai
from google.genai import types


@dataclass
class LLMResult:
    text: str
    input_tokens: int
    output_tokens: int


class LLMProvider(ABC):
    provider_name = "Unknown"
    model = "unknown"

    @abstractmethod
    def generate(self, prompt):
        raise NotImplementedError


class GeminiProvider(LLMProvider):
    provider_name = "Gemini"

    def __init__(self, api_key, model=None):
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
        self.client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(timeout=60000),
        )

    def generate(self, prompt):
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        usage = getattr(response, "usage_metadata", None)
        input_count = getattr(usage, "prompt_token_count", 0) or 0
        output_count = getattr(usage, "candidates_token_count", 0) or 0
        return LLMResult(
            text=response.text or "",
            input_tokens=input_count,
            output_tokens=output_count,
        )


class OllamaProvider(LLMProvider):
    provider_name = "Ollama"

    def __init__(self, model=None, url=None):
        self.model = model or os.getenv("OLLAMA_MODEL", "qwen3.5:4b")
        self.url = url or os.getenv(
            "OLLAMA_URL", "http://localhost:11434/api/generate"
        )

    def generate(self, prompt):
        response = requests.post(
            self.url,
            json={"model": self.model, "prompt": prompt, "stream": False},
            timeout=(5, 180),
        )
        response.raise_for_status()
        data = response.json()
        return LLMResult(
            text=data.get("response", ""),
            input_tokens=data.get("prompt_eval_count", 0) or 0,
            output_tokens=data.get("eval_count", 0) or 0,
        )


class LLMClient:
    RETRYABLE_HTTP_CODES = (408, 429, 500, 502, 503, 504)

    def __init__(self, provider, usage_logger):
        self.provider = provider
        self.usage_logger = usage_logger

    def generate(self, prompt):
        start = time.perf_counter()
        max_attempts = 3

        for attempt in range(max_attempts):
            try:
                result = self.provider.generate(prompt)
                latency_ms = round((time.perf_counter() - start) * 1000, 2)

                if self.provider.provider_name == "Gemini":
                    input_rate = float(os.getenv("GEMINI_INPUT_PRICE_PER_MILLION", "0"))
                    output_rate = float(os.getenv("GEMINI_OUTPUT_PRICE_PER_MILLION", "0"))
                    cost = (
                        result.input_tokens * input_rate
                        + result.output_tokens * output_rate
                    ) / 1_000_000
                    cost_type = "estimated_hosted_api_cost"
                else:
                    cost = 0.0
                    cost_type = "local_inference_cost_not_included"

                self.usage_logger.log_call({
                    "provider": self.provider.provider_name,
                    "model": self.provider.model,
                    "input_tokens": result.input_tokens,
                    "output_tokens": result.output_tokens,
                    "total_tokens": result.input_tokens + result.output_tokens,
                    "latency_ms": latency_ms,
                    "estimated_cost_usd": round(cost, 8),
                    "cost_type": cost_type,
                    "status": "success",
                    "attempts": attempt + 1,
                })

                print(f"Latency: {latency_ms} ms")
                print(f"Input tokens: {result.input_tokens}")
                print(f"Output tokens: {result.output_tokens}")
                print(f"Estimated cost (USD): {cost}")
                return result.text

            except Exception as error:
                status = getattr(error, "status_code", None)
                if status is None:
                    status = getattr(error, "code", None)
                error_name = type(error).__name__.lower()
                retryable = (
                    isinstance(error, (
                        requests.exceptions.Timeout,
                        requests.exceptions.ConnectionError,
                    ))
                    or status in self.RETRYABLE_HTTP_CODES
                    or "timeout" in error_name
                    or "unavailable" in error_name
                    or "resourceexhausted" in error_name
                )

                if not retryable or attempt == max_attempts - 1:
                    latency_ms = round((time.perf_counter() - start) * 1000, 2)
                    self.usage_logger.log_call({
                        "provider": self.provider.provider_name,
                        "model": self.provider.model,
                        "input_tokens": None,
                        "output_tokens": None,
                        "total_tokens": None,
                        "latency_ms": latency_ms,
                        "estimated_cost_usd": None,
                        "status": "failed",
                        "attempts": attempt + 1,
                        "error": str(error),
                    })
                    raise

                delay = 2 ** attempt
                print(
                    f"Temporary error. Retry {attempt + 1} of "
                    f"{max_attempts - 1} in {delay} seconds."
                )
                time.sleep(delay)
