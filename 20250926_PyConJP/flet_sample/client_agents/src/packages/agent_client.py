"""OpenAI client management for Hello Agent app."""

import traceback
from typing import Optional

from openai import AsyncOpenAI

from .config import get_openai_api_key


class AgentClient:
    """Manages OpenAI API client and agent interactions."""

    def __init__(self):
        self.client: Optional[AsyncOpenAI] = None
        self.is_initialized = False

    async def initialize(self) -> tuple[bool, str]:
        """
        Initialize the OpenAI client.

        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            api_key = get_openai_api_key()
            if not api_key or api_key == "your-openai-api-key-here":
                return False, "API key not configured properly"

            self.client = AsyncOpenAI(api_key=api_key)

            # Test the connection
            await self.client.models.list()

            self.is_initialized = True
            return True, "OpenAI client initialized successfully"

        except Exception as error:
            error_msg = f"Initialization failed: {str(error)}"
            print(f"Full error: {traceback.format_exc()}")
            return False, error_msg

    async def run_agent(self, prompt: str, instructions: str = "") -> tuple[bool, str]:
        """
        Run the agent with given prompt and instructions.

        Args:
            prompt: The user prompt
            instructions: System instructions for the agent

        Returns:
            tuple: (success: bool, result: str)
        """
        if not self.is_initialized or not self.client:
            return False, "Client not initialized"

        if not prompt.strip():
            return False, "Please enter a prompt"

        try:
            # Create the system message with instructions
            messages = [
                {"role": "system", "content": instructions},
                {"role": "user", "content": prompt},
            ]

            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7,
            )

            result = response.choices[0].message.content.strip()

            if result:
                return True, result
            else:
                return False, "Agent returned empty response"

        except Exception as error:
            error_msg = f"Agent execution failed: {str(error)}"
            print(f"Full error: {traceback.format_exc()}")
            return False, error_msg
