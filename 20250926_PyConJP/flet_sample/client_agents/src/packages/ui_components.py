"""UI components for Hello Agent app."""

import flet as ft


class UIComponents:
    """Factory class for creating UI components."""

    @staticmethod
    def create_header() -> ft.Container:
        """Create the header section."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Hello Agent! 🤖", size=28, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        "A simple demo showing how to create AI agents using OpenAI API in Flet.",
                        size=14,
                        color=ft.Colors.GREY_700,
                    ),
                ]
            ),
            padding=20,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=10,
            margin=ft.margin.only(bottom=20),
        )

    @staticmethod
    def create_description() -> ft.Container:
        """Create the description section."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("How it works:", weight=ft.FontWeight.BOLD),
                    ft.Text("• Configure: Set your OpenAI API key in the .env file"),
                    ft.Text("• Initialize: Set up the OpenAI client"),
                    ft.Text("• Customize: Choose prompts and agent instructions"),
                    ft.Text("• Run: Send your prompt to the agent and see responses"),
                ]
            ),
            padding=15,
            bgcolor=ft.Colors.GREY_50,
            border_radius=5,
            border=ft.border.all(1, ft.Colors.GREY_300),
            margin=ft.margin.only(bottom=20),
        )

    @staticmethod
    def create_config_container(config_status: ft.Text) -> ft.Container:
        """Create the configuration status container."""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Text("📋 Configuration: ", weight=ft.FontWeight.BOLD),
                    config_status,
                ]
            ),
            padding=10,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=5,
            margin=ft.margin.only(bottom=20),
        )

    @staticmethod
    def create_prompt_examples(set_prompt_callback) -> ft.Row:
        """Create prompt example buttons."""
        return ft.Row(
            [
                ft.Text("Quick examples:", size=12),
                ft.ElevatedButton(
                    "Recursion",
                    on_click=lambda e: set_prompt_callback(
                        "Tell me about recursion in programming in just a few sentences."
                    ),
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE, bgcolor=ft.Colors.GREY_600
                    ),
                ),
                ft.ElevatedButton(
                    "AI Poem",
                    on_click=lambda e: set_prompt_callback(
                        "Write a short poem about artificial intelligence."
                    ),
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE, bgcolor=ft.Colors.GREY_600
                    ),
                ),
                ft.ElevatedButton(
                    "Quantum Computing",
                    on_click=lambda e: set_prompt_callback(
                        "Explain quantum computing in simple terms and just a few sentences."
                    ),
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE, bgcolor=ft.Colors.GREY_600
                    ),
                ),
                ft.ElevatedButton(
                    "Philosophy",
                    on_click=lambda e: set_prompt_callback(
                        "What is the meaning of life?"
                    ),
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE, bgcolor=ft.Colors.GREY_600
                    ),
                ),
            ],
            wrap=True,
        )

    @staticmethod
    def create_instruction_examples(set_instructions_callback) -> ft.Row:
        """Create instruction example buttons."""
        return ft.Row(
            [
                ft.Text("Instruction examples:", size=12),
                ft.ElevatedButton(
                    "Haiku Bot",
                    on_click=lambda e: set_instructions_callback(
                        "You only respond in haikus."
                    ),
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE, bgcolor=ft.Colors.GREY_600
                    ),
                ),
                ft.ElevatedButton(
                    "Code Helper",
                    on_click=lambda e: set_instructions_callback(
                        "You are a helpful programming assistant. Always provide code examples."
                    ),
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE, bgcolor=ft.Colors.GREY_600
                    ),
                ),
                ft.ElevatedButton(
                    "Pirate",
                    on_click=lambda e: set_instructions_callback(
                        "You speak like a pirate. Arrr!"
                    ),
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE, bgcolor=ft.Colors.GREY_600
                    ),
                ),
                ft.ElevatedButton(
                    "Philosopher",
                    on_click=lambda e: set_instructions_callback(
                        "You are a wise philosopher who speaks in metaphors."
                    ),
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE, bgcolor=ft.Colors.GREY_600
                    ),
                ),
            ],
            wrap=True,
        )

    @staticmethod
    def create_running_indicator() -> ft.Container:
        """Create the running indicator."""
        return ft.Container(
            content=ft.Row(
                [
                    ft.ProgressRing(width=20, height=20),
                    ft.Text("🐍 Running Python code...", weight=ft.FontWeight.BOLD),
                ]
            ),
            padding=15,
            bgcolor=ft.Colors.AMBER_100,
            border_radius=5,
            border=ft.border.all(1, ft.Colors.AMBER_300),
            visible=False,
        )
