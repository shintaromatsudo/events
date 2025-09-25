import base64
import threading
import time
from typing import Callable, Optional

import cv2


class CameraProcessor:
    """カメラの処理とぼかし効果を管理するクラス"""

    def __init__(self):
        self.camera: Optional[cv2.VideoCapture] = None
        self.is_running = False
        self.blur_strength = 15
        self.camera_thread: Optional[threading.Thread] = None
        self.frame_callback: Optional[Callable[[str], None]] = None
        self.error_callback: Optional[Callable[[str], None]] = None
        self.face_detection_enabled = True

        # OpenCVのHaar Cascade分類器を読み込み
        try:
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            )
            if self.face_cascade.empty():
                print("顔検出分類器の読み込みに失敗しました")
                self.face_detection_enabled = False
        except Exception as e:
            print(f"顔検出分類器の初期化エラー: {e}")
            self.face_detection_enabled = False

    def set_frame_callback(self, callback: Callable[[str], None]):
        """フレーム更新時のコールバックを設定"""
        self.frame_callback = callback

    def set_error_callback(self, callback: Callable[[str], None]):
        """エラー発生時のコールバックを設定"""
        self.error_callback = callback

    def set_blur_strength(self, strength: int):
        """ぼかし強度を設定（奇数に調整）"""
        self.blur_strength = strength if strength % 2 == 1 else strength + 1

    def start_camera(self) -> bool:
        """カメラを開始

        Returns:
            bool: 開始に成功した場合True
        """
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                if self.error_callback:
                    self.error_callback("カメラが見つかりません")
                return False

            # カメラ設定
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.camera.set(cv2.CAP_PROP_FPS, 30)

            self.is_running = True

            # 別スレッドでカメラ処理を開始
            self.camera_thread = threading.Thread(target=self._camera_loop)
            self.camera_thread.daemon = True
            self.camera_thread.start()

            return True

        except Exception as ex:
            if self.error_callback:
                self.error_callback(f"エラー: {str(ex)}")
            return False

    def stop_camera(self):
        """カメラを停止"""
        self.is_running = False
        if self.camera:
            self.camera.release()
            self.camera = None

    def _camera_loop(self):
        """カメラ映像の処理ループ（内部メソッド）"""
        while self.is_running and self.camera:
            try:
                ret, frame = self.camera.read()
                if not ret:
                    break

                # フレームを水平反転（鏡像効果）
                frame = cv2.flip(frame, 1)

                # 顔検出とぼかし処理を適用
                processed_frame = self._apply_face_blur(frame)

                # フレームをBase64エンコード
                encoded_image = self._frame_to_base64(processed_frame)

                # コールバックでフレームを通知
                if self.frame_callback:
                    self.frame_callback(encoded_image)

                # FPS制御
                time.sleep(1 / 30)  # 30 FPS

            except Exception as ex:
                if self.error_callback:
                    self.error_callback(f"カメラループエラー: {ex}")
                break

    def _apply_face_blur(self, frame):
        """顔検出を行い、顔以外の部分にぼかしを適用

        Args:
            frame: OpenCVフレーム

        Returns:
            処理済みフレーム
        """
        if not self.face_detection_enabled:
            # 顔検出が無効の場合は全体にぼかしを適用
            return cv2.GaussianBlur(frame, (self.blur_strength, self.blur_strength), 0)

        # グレースケールに変換（顔検出用）
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 顔を検出
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )

        # 全体にぼかしを適用
        blurred_frame = cv2.GaussianBlur(
            frame, (self.blur_strength, self.blur_strength), 0
        )

        # 顔部分を元のフレームで復元
        result_frame = blurred_frame.copy()
        for x, y, w, h in faces:
            # 顔部分を元の画像から切り出して復元
            result_frame[y : y + h, x : x + w] = frame[y : y + h, x : x + w]

        return result_frame

    def _frame_to_base64(self, frame) -> str:
        """OpenCVフレームをBase64文字列に変換

        Args:
            frame: OpenCVフレーム

        Returns:
            str: Base64エンコードされた画像データ
        """
        # OpenCVでJPEGエンコード
        _, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])

        # Base64エンコード
        encoded_image = base64.b64encode(buffer).decode("utf-8")
        return encoded_image

    def is_camera_running(self) -> bool:
        """カメラが動作中かどうかを確認"""
        return self.is_running
