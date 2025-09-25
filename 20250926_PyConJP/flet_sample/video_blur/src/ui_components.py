from typing import Callable, Optional

import flet as ft


class VideoBlurUI:
    """ビデオぼかしアプリのUIコンポーネント"""

    def __init__(self, page: ft.Page):
        self.page = page
        self._setup_page()

        # コールバック関数
        self.start_camera_callback: Optional[Callable] = None
        self.stop_camera_callback: Optional[Callable] = None
        self.blur_change_callback: Optional[Callable[[int], None]] = None

        # UI要素を初期化
        self._create_ui_elements()
        self._setup_layout()

    def _setup_page(self):
        """ページの基本設定"""
        self.page.title = "リアルタイム映像ぼかしアプリ"
        self.page.theme_mode = ft.ThemeMode.LIGHT

    def _create_ui_elements(self):
        """UI要素を作成"""
        # 映像表示エリア
        self.video_frame = ft.Image(
            width=640,
            height=480,
            fit=ft.ImageFit.CONTAIN,
            border_radius=ft.border_radius.all(10),
        )

        # ぼかし強度スライダー
        self.blur_slider = ft.Slider(
            min=1,
            max=50,
            divisions=49,
            value=45,
            label="ぼかし強度: {value}",
            on_change=self._on_blur_change,
        )

        # 開始ボタン
        self.start_button = ft.ElevatedButton(
            text="カメラ開始",
            icon="play_arrow",
            on_click=self._on_start_camera,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.GREEN,
            ),
        )

        # 停止ボタン
        self.stop_button = ft.ElevatedButton(
            text="カメラ停止",
            icon="stop",
            on_click=self._on_stop_camera,
            disabled=True,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.RED,
            ),
        )

        # ステータステキスト
        self.status_text = ft.Text(
            "カメラは停止中です",
            size=16,
            color=ft.Colors.GREY_700,
        )

    def _setup_layout(self):
        """レイアウトをセットアップ"""
        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        # タイトル
                        ft.Container(
                            content=ft.Text(
                                "リアルタイム映像ぼかしアプリ",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_900,
                            ),
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(bottom=20),
                        ),
                        # 映像表示エリア
                        ft.Container(
                            content=self.video_frame,
                            alignment=ft.alignment.center,
                            border=ft.border.all(2, ft.Colors.GREY_400),
                            border_radius=ft.border_radius.all(10),
                            padding=10,
                            bgcolor=ft.Colors.GREY_100,
                        ),
                        # コントロールパネル
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(
                                        "ぼかし強度",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    self.blur_slider,
                                    ft.Row(
                                        [
                                            self.start_button,
                                            self.stop_button,
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=20,
                                    ),
                                    self.status_text,
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=15,
                            ),
                            padding=20,
                            border_radius=ft.border_radius.all(10),
                            bgcolor=ft.Colors.WHITE,
                            border=ft.border.all(1, ft.Colors.GREY_300),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                padding=30,
                expand=True,
            )
        )

    # コールバック設定メソッド
    def set_start_camera_callback(self, callback: Callable):
        """カメラ開始コールバックを設定"""
        self.start_camera_callback = callback

    def set_stop_camera_callback(self, callback: Callable):
        """カメラ停止コールバックを設定"""
        self.stop_camera_callback = callback

    def set_blur_change_callback(self, callback: Callable[[int], None]):
        """ぼかし強度変更コールバックを設定"""
        self.blur_change_callback = callback

    # イベントハンドラー
    def _on_blur_change(self, e):
        """ぼかし強度の変更時の処理"""
        if self.blur_change_callback:
            value = int(e.control.value)
            self.blur_change_callback(value)

    def _on_start_camera(self, e):
        """カメラ開始ボタンクリック時の処理"""
        if self.start_camera_callback:
            self.start_camera_callback()

    def _on_stop_camera(self, e):
        """カメラ停止ボタンクリック時の処理"""
        if self.stop_camera_callback:
            self.stop_camera_callback()

    # UI更新メソッド
    def update_video_frame(self, base64_image: str):
        """映像フレームを更新"""
        self.video_frame.src_base64 = base64_image
        self.page.update()

    def clear_video_frame(self):
        """映像フレームをクリア"""
        self.video_frame.src = None
        self.page.update()

    def update_status(self, message: str, color: str = ft.Colors.GREY_700):
        """ステータステキストを更新"""
        self.status_text.value = message
        self.status_text.color = color
        self.page.update()

    def set_camera_running(self, is_running: bool):
        """カメラの実行状態に応じてボタンの状態を更新"""
        self.start_button.disabled = is_running
        self.stop_button.disabled = not is_running
        self.page.update()

    def get_blur_strength(self) -> int:
        """現在のぼかし強度を取得"""
        return int(self.blur_slider.value)
