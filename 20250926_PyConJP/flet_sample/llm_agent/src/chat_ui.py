import flet as ft


class ChatUI:
    """チャットUIを管理するクラス"""

    def __init__(self, llm_client):
        self.llm_client = llm_client
        self._setup_ui()

    def _setup_ui(self):
        """UIコンポーネントを初期化"""
        self.chat_history = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)

        self.user_input = ft.TextField(
            hint_text="Ask me anything...",
            expand=True,
            on_submit=lambda e: self.handle_submit(e.control.value),
        )

        self.send_button = ft.IconButton(
            icon=ft.Icons.SEND,
            on_click=lambda e: self.handle_submit(self.user_input.value),
        )

    def handle_submit(self, message: str):
        """メッセージ送信を処理"""
        if not message:
            return
        self.add_user_message(message)
        self.clear_input()
        self.set_input_disabled(True)
        self.add_ai_message("Gemini: ")

        try:
            response = self.llm_client.generate_content_stream(message)
            for chunk in response:
                self.add_ai_message(chunk.text)
        except Exception as e:
            self.add_ai_message(f"Error: {str(e)}")
        finally:
            self.set_input_disabled(False)

    def add_user_message(self, message: str):
        """ユーザーメッセージをチャット履歴に追加"""
        self.chat_history.controls.append(
            ft.Text(f"You: {message}", selectable=True)
        )
        self.chat_history.update()

    def add_ai_message(self, message: str):
        """AIメッセージをチャット履歴に追加"""
        self.chat_history.controls.append(
            ft.Text(message, selectable=True)
        )
        self.chat_history.update()

    def clear_input(self):
        """入力フィールドをクリア"""
        self.user_input.value = ""
        self.user_input.update()

    def set_input_disabled(self, disabled: bool):
        """入力フィールドの有効/無効を設定"""
        self.user_input.disabled = disabled
        self.user_input.update()

    def get_layout(self) -> ft.Container:
        """UIレイアウトを取得"""
        return ft.Container(
            content=ft.Column(
                [
                    self.chat_history,
                    ft.Row(
                        [
                            self.user_input,
                            self.send_button,
                        ]
                    ),
                ],
                expand=True,
            ),
            expand=True,
        )
