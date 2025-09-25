"""Main application class for Hello Agent app."""

import flet as ft

from .agent_client import AgentClient
from .config import is_api_key_configured
from .ui_components import UIComponents


class HelloAgentApp:
    """Main application class for Hello Agent."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.agent_client = AgentClient()

        # UI elements
        self.config_status = ft.Text()
        self.init_btn = ft.ElevatedButton()
        self.init_output = ft.TextField()
        self.prompt_input = ft.TextField()
        self.instructions_input = ft.TextField()
        self.run_btn = ft.ElevatedButton()
        self.clear_btn = ft.ElevatedButton()
        self.agent_output = ft.TextField()
        self.running_indicator = ft.Container()

        self.setup_ui()
        self.check_config()

    def check_config(self):
        """Check API key configuration and update UI accordingly."""
        if not is_api_key_configured():
            self.config_status.value = "⚠️ Please set your API key in .env file"
            self.config_status.color = ft.Colors.AMBER
            self.init_btn.disabled = True
        else:
            self.config_status.value = "✅ API key configured"
            self.config_status.color = ft.Colors.GREEN
            self.init_btn.disabled = False
        self.page.update()

    def setup_ui(self):
        """Set up the user interface."""
        self.page.title = "Hello Agent! - Flet Version"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.scroll = ft.ScrollMode.AUTO

        # Create UI components
        header = UIComponents.create_header()
        description = UIComponents.create_description()
        config_container = UIComponents.create_config_container(self.config_status)

        # Initialize button
        self.init_btn = ft.ElevatedButton(
            "⚙️ Initialize OpenAI Client",
            on_click=self.initialize_client,
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
        )

        # Initialize output
        self.init_output = ft.TextField(
            value="Click 'Initialize OpenAI Client' to set up the environment...",
            multiline=True,
            min_lines=3,
            max_lines=5,
            read_only=True,
            bgcolor=ft.Colors.GREY_100,
        )

        # Prompt input
        self.prompt_input = ft.TextField(
            label="Custom Prompt",
            value="Tell me about recursion in programming in just a few sentences.",
            multiline=True,
            min_lines=2,
            max_lines=4,
        )

        # Example prompt buttons
        prompt_examples = UIComponents.create_prompt_examples(self.set_prompt)

        # Instructions input
        self.instructions_input = ft.TextField(
            label="Agent Instructions",
            value="You only respond in haikus.",
            multiline=True,
            min_lines=2,
            max_lines=4,
        )

        # Example instruction buttons
        instruction_examples = UIComponents.create_instruction_examples(
            self.set_instructions
        )

        # Action buttons
        self.run_btn = ft.ElevatedButton(
            "🚀 Run Agent",
            on_click=self.run_agent,
            disabled=True,
            bgcolor=ft.Colors.GREEN,
            color=ft.Colors.WHITE,
        )

        self.clear_btn = ft.ElevatedButton(
            "🗑️ Clear Agent Output",
            on_click=self.clear_output,
            disabled=True,
            style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.RED),
        )

        action_buttons = ft.Row([self.run_btn, self.clear_btn])

        # Running indicator
        self.running_indicator = UIComponents.create_running_indicator()

        # Agent output
        self.agent_output = ft.TextField(
            value="Initialize the OpenAI client first, then click 'Run Agent' to test the agent",
            multiline=True,
            min_lines=10,
            max_lines=20,
            read_only=True,
            bgcolor=ft.Colors.GREY_100,
        )

        # Main container
        main_container = ft.Container(
            content=ft.Column(
                [
                    header,
                    description,
                    config_container,
                    self.init_btn,
                    ft.Container(
                        self.init_output, margin=ft.margin.only(top=10, bottom=20)
                    ),
                    ft.Container(
                        content=ft.Column([self.prompt_input, prompt_examples]),
                        margin=ft.margin.only(bottom=20),
                    ),
                    ft.Container(
                        content=ft.Column(
                            [self.instructions_input, instruction_examples]
                        ),
                        margin=ft.margin.only(bottom=20),
                    ),
                    action_buttons,
                    self.running_indicator,
                    ft.Container(self.agent_output, margin=ft.margin.only(top=20)),
                ],
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=30,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.GREY_300),
            margin=20,
        )

        self.page.add(main_container)

    def set_prompt(self, text: str):
        """Set the prompt input text."""
        self.prompt_input.value = text
        self.page.update()

    def set_instructions(self, text: str):
        """Set the instructions input text."""
        self.instructions_input.value = text
        self.page.update()

    def log_init(self, message: str, level: str = "info"):
        """Log a message to the initialization output."""
        prefix = {"info": "ℹ️", "success": "✅", "error": "❌", "warning": "⚠️"}.get(
            level, "ℹ️"
        )
        current_text = self.init_output.value
        new_text = f"{current_text}\n{prefix} {message}"
        self.init_output.value = new_text
        self.page.update()

    def log_agent(self, message: str, level: str = "info"):
        """Log a message to the agent output."""
        prefix = {"info": "ℹ️", "success": "✅", "error": "❌", "warning": "⚠️"}.get(
            level, "ℹ️"
        )
        current_text = self.agent_output.value
        new_text = f"{current_text}\n{prefix} {message}"
        self.agent_output.value = new_text
        self.page.update()

    async def initialize_client(self, e):
        """Initialize the OpenAI client."""
        self.init_btn.disabled = True
        self.init_btn.text = "Initializing..."
        self.page.update()

        try:
            self.log_init("🚀 Initializing OpenAI client...")
            self.log_init("🧪 Testing API connection...")

            success, message = await self.agent_client.initialize()

            if success:
                self.log_init("📡 API connection successful", "success")
                self.log_init(f"✅ {message}", "success")

                self.init_btn.text = "✅ Environment Ready"
                self.run_btn.disabled = False
                self.clear_btn.disabled = False
            else:
                self.log_init(message, "error")
                self.init_btn.disabled = False
                self.init_btn.text = "⚙️ Initialize OpenAI Client"

        except Exception as error:
            self.log_init(f"Unexpected error: {str(error)}", "error")
            self.init_btn.disabled = False
            self.init_btn.text = "⚙️ Initialize OpenAI Client"

        self.page.update()

    def show_running(self, show: bool = True):
        """Show or hide the running indicator."""
        self.running_indicator.visible = show
        self.page.update()

    async def run_agent(self, e):
        """Run the agent with current prompt and instructions."""
        prompt = self.prompt_input.value.strip()
        instructions = self.instructions_input.value.strip()

        self.run_btn.disabled = True
        self.show_running(True)

        try:
            self.log_agent("🤖 Setting up agent and running...")
            self.log_agent(f'Instructions: "{instructions}"')
            self.log_agent(f'Prompt: "{prompt}"')
            self.log_agent("🔄 Sending request to OpenAI...")

            success, result = await self.agent_client.run_agent(prompt, instructions)

            if success:
                self.log_agent("🎉 Agent response received successfully!", "success")
                self.log_agent("")
                self.log_agent("📝 AGENT RESPONSE:", "info")
                self.log_agent("─" * 50)
                self.log_agent(result)
                self.log_agent("─" * 50)
            else:
                self.log_agent(result, "error")

        except Exception as error:
            self.log_agent(f"Unexpected error: {str(error)}", "error")
        finally:
            self.run_btn.disabled = False
            self.show_running(False)

    def clear_output(self, e):
        """Clear the agent output."""
        self.agent_output.value = (
            "Agent output cleared. Run the agent to see new responses."
        )
        self.page.update()
