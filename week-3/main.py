import os
from dotenv import load_dotenv

from llm_client import GeminiProvider, OllamaProvider, LLMClient
from usage_logger import UsageLogger


def main():
    load_dotenv(override=True)

    api_key = os.getenv("GEMINI_API_KEY", "")
    usage_logger = UsageLogger()

    try:
        provider_name = input("Choose provider (gemini/ollama): ").strip().lower()

        if provider_name == "gemini":
            if not api_key or api_key == "PASTE_YOUR_GEMINI_API_KEY_HERE":
                raise ValueError("Add your real GEMINI_API_KEY to .env first.")
            provider = GeminiProvider(api_key)
        elif provider_name == "ollama":
            provider = OllamaProvider()
        else:
            raise ValueError("Invalid provider. Type gemini or ollama.")

        client = LLMClient(provider, usage_logger)
        prompt = input("Enter your question: ").strip()
        if not prompt:
            raise ValueError("Question cannot be empty.")

        answer = client.generate(prompt)
        print("\nLLM Response:")
        print(answer)
    finally:
        usage_logger.close()


if __name__ == "__main__":
    main()
