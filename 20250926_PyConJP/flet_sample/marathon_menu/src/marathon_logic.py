"""
マラソン練習メニュー生成のロジック
"""
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Tuple, NamedTuple


class RunnerLevel(Enum):
    """ランナーレベル"""
    ADVANCED = "上級者"
    INTERMEDIATE = "中級者"
    BEGINNER = "初心者"


@dataclass(frozen=True)
class LevelConfig:
    """レベル別設定"""
    level: RunnerLevel
    time_threshold: float  # 分
    base_jog: int  # km
    long_run: int  # km


class TrainingSchedule(NamedTuple):
    """トレーニングスケジュール"""
    level: RunnerLevel
    base_jog: int
    long_run: int
    pace: str


class MarathonTimeError(ValueError):
    """マラソンタイム関連のエラー"""
    pass


class MarathonMenuGenerator:
    """マラソン練習メニューを生成するクラス"""

    # 定数
    MARATHON_DISTANCE = 42.195  # km
    MIN_RECOVERY_JOG_DISTANCE = 3  # km
    INTERVAL_BASE_SETS = 12

    def __init__(self):
        self.level_configs = [
            LevelConfig(RunnerLevel.ADVANCED, 180, 12, 25),    # 3時間未満
            LevelConfig(RunnerLevel.INTERMEDIATE, 240, 10, 20), # 4時間未満
            LevelConfig(RunnerLevel.BEGINNER, float('inf'), 8, 15), # 4時間以上
        ]

    def parse_time(self, time_str: str) -> float:
        """時間文字列をパースして総分数を返す

        Args:
            time_str: "時:分:秒"形式の文字列

        Returns:
            総分数

        Raises:
            MarathonTimeError: 時間形式が正しくない場合
        """
        if not time_str or not time_str.strip():
            raise MarathonTimeError("時間を入力してください")

        time_parts = time_str.split(":")
        if len(time_parts) != 3:
            raise MarathonTimeError("時間形式が正しくありません。時:分:秒の形式で入力してください")

        try:
            hours = int(time_parts[0])
            minutes = int(time_parts[1])
            seconds = int(time_parts[2])
        except ValueError:
            raise MarathonTimeError("時間には数値を入力してください")

        if hours < 0 or minutes < 0 or seconds < 0:
            raise MarathonTimeError("時間には正の数値を入力してください")

        if minutes >= 60 or seconds >= 60:
            raise MarathonTimeError("分・秒は60未満で入力してください")

        return hours * 60 + minutes + seconds / 60

    def determine_level(self, total_minutes: float) -> LevelConfig:
        """目標タイムからレベル設定を決定

        Args:
            total_minutes: 総分数

        Returns:
            レベル設定
        """
        for config in self.level_configs:
            if total_minutes < config.time_threshold:
                return config

        # デフォルトは初心者レベル
        return self.level_configs[-1]

    def calculate_pace(self, total_minutes: float) -> str:
        """目標ペースを計算

        Args:
            total_minutes: 総分数

        Returns:
            "分:秒/km"形式の文字列
        """
        pace_minutes = total_minutes / self.MARATHON_DISTANCE
        minutes = int(pace_minutes)
        seconds = int((pace_minutes - minutes) * 60)
        return f"{minutes}:{seconds:02d}/km"

    def generate_weekly_menu(self, base_jog: int, long_run: int, increment: int) -> Dict[str, str]:
        """週間練習メニューを生成

        Args:
            base_jog: ベースジョギング距離
            long_run: ロング走距離
            increment: 増加量

        Returns:
            曜日と練習内容の辞書
        """
        easy_jog_distance = max(base_jog - 2, 3)  # 最小3km
        interval_sets = self.INTERVAL_BASE_SETS - increment
        long_run_range_start = max(long_run - 5, 10)  # 最小10km

        return {
            "月曜日": "休息日",
            "火曜日": f"ジョギング {easy_jog_distance}km (ゆっくり)",
            "水曜日": f"インターバル走 1km×{interval_sets}本",
            "木曜日": f"ジョギング {base_jog}km (ペース走)",
            "金曜日": "休息日",
            "土曜日": f"ロング走 {long_run_range_start}〜{long_run}km",
            "日曜日": f"軽いジョギング {self.MIN_RECOVERY_JOG_DISTANCE}km (リカバリー)",
        }

    def _generate_menu_text(self, target_time: str, months: int) -> str:
        """練習メニューを生成

        Args:
            target_time: 目標タイム（"時:分:秒"形式）
            months: 何ヶ月後

        Returns:
            練習メニューの文字列

        Raises:
            ValueError: 入力値が不正な場合
        """
        if not target_time or months <= 0:
            raise ValueError("目標タイムと期間を正しく入力してください")

        # 目標タイムをパース
        total_minutes = self.parse_time(target_time)

        # レベル判定
        level_config = self.determine_level(total_minutes)

        # 期間に応じた調整
        increment = months
        adjusted_base_jog = level_config.base_jog - increment
        adjusted_long_run = level_config.long_run - increment * 2

        # 目標ペース計算
        pace = self.calculate_pace(total_minutes)

        # 週間メニュー生成
        weekly_menu = self.generate_weekly_menu(adjusted_base_jog, adjusted_long_run, increment)

        # メニュー文字列作成
        menu_text = f"""🏃‍♂️ 今週の練習メニュー

目標: {target_time} ({level_config.level.value}レベル)
期間: {months}ヶ月後
目標ペース: {pace}

📅 週間メニュー:
{chr(10).join([f"- {day}: {activity}" for day, activity in weekly_menu.items()])}

💡 ポイント:
・無理をせず段階的に距離を伸ばしましょう
・水分補給を忘れずに
・体調不良時は無理をしないでください"""

        return menu_text

    def generate_menu(self, target_time_value: str, target_months_value: str) -> tuple[str, bool]:
        """メニュー生成処理を実行

        Args:
            target_time_value: 目標タイムの入力値
            target_months_value: 期間の入力値

        Returns:
            (結果メッセージ, 成功フラグ)
        """
        try:
            # 入力値の処理
            time_str = target_time_value.strip() if target_time_value else ""
            months = int(target_months_value) if target_months_value and target_months_value.strip() else 0

            # メニュー生成
            menu_text = self._generate_menu_text(time_str, months)
            return menu_text, True

        except MarathonTimeError as mte:
            return f"時間入力エラー: {str(mte)}", False
        except ValueError as ve:
            return f"入力エラー: {str(ve)}", False
        except Exception as ex:
            return f"予期しないエラー: {str(ex)}", False

if __name__ == "__main__":
    # 引数を受け取る
    import sys
    generator = MarathonMenuGenerator()
    menu, success = generator.generate_menu(sys.argv[1], sys.argv[2])
    print(menu)
