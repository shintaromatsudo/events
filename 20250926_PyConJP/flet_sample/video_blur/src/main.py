import flet as ft
from camera_logic import CameraProcessor
from ui_components import VideoBlurUI


class VideoBlurApp:
    """ビデオぼかしアプリケーションのメインクラス

    UIコンポーネントとカメラ処理ロジックを統合します。
    """

    def __init__(self, page: ft.Page):
        self.page = page

        # UIコンポーネントを初期化
        self.ui = VideoBlurUI(page)

        # カメラ処理ロジックを初期化
        self.camera_processor = CameraProcessor()

        # コールバックを設定
        self._setup_callbacks()

        # 初期ぼかし強度を設定
        initial_blur = self.ui.get_blur_strength()
        self.camera_processor.set_blur_strength(initial_blur)

    def _setup_callbacks(self):
        """UIとロジック間のコールバックを設定"""
        # UIからロジックへのコールバック
        self.ui.set_start_camera_callback(self._on_start_camera)
        self.ui.set_stop_camera_callback(self._on_stop_camera)
        self.ui.set_blur_change_callback(self._on_blur_change)

        # ロジックからUIへのコールバック
        self.camera_processor.set_frame_callback(self._on_frame_update)
        self.camera_processor.set_error_callback(self._on_error)

    def _on_start_camera(self):
        """カメラ開始処理"""
        success = self.camera_processor.start_camera()
        if success:
            self.ui.set_camera_running(True)
            self.ui.update_status("カメラが動作中です", ft.Colors.GREEN)
        # エラーの場合は camera_processor からエラーコールバックが呼ばれる

    def _on_stop_camera(self):
        """カメラ停止処理"""
        self.camera_processor.stop_camera()
        self.ui.set_camera_running(False)
        self.ui.update_status("カメラは停止中です", ft.Colors.GREY_700)
        self.ui.clear_video_frame()

    def _on_blur_change(self, strength: int):
        """ぼかし強度変更処理"""
        self.camera_processor.set_blur_strength(strength)

    def _on_frame_update(self, base64_image: str):
        """フレーム更新処理"""
        self.ui.update_video_frame(base64_image)

    def _on_error(self, error_message: str):
        """エラー処理"""
        self.ui.update_status(error_message, ft.Colors.RED)


def main(page: ft.Page):
    """メイン関数"""
    VideoBlurApp(page)


if __name__ == "__main__":
    ft.app(main)
