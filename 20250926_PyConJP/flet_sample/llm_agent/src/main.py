import flet as ft
from gemini_client import GeminiClient
from chat_ui import ChatUI


class ChatApp:
    """チャットアプリケーションのメインクラス"""

    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Gemini API Demo"

        self.gemini_client = GeminiClient()
        self.chat_ui = ChatUI(llm_client=self.gemini_client)

        # UIを設定
        self.page.add(self.chat_ui.get_layout())


def main(page: ft.Page):
    """アプリケーションのエントリーポイント"""
    ChatApp(page)

ft.app(main)
