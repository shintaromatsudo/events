"""Entry point for Hello Agent app."""

import flet as ft
from packages.hello_agent_app import HelloAgentApp


def main(page: ft.Page):
    """Main entry point for the application."""
    HelloAgentApp(page)


if __name__ == "__main__":
    ft.app(main)
