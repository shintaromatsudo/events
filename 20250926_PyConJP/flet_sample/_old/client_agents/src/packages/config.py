"""Configuration management for Hello Agent app."""

import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_openai_api_key() -> str | None:
    """Get OpenAI API key from environment variables."""
    return os.getenv("OPENAI_API_KEY")


def is_api_key_configured() -> bool:
    """Check if OpenAI API key is properly configured."""
    api_key = get_openai_api_key()
    return api_key is not None and api_key != "your-openai-api-key-here"
