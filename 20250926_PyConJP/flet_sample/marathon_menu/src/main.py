import flet as ft
from marathon_logic import MarathonMenuGenerator


def main(page: ft.Page):
    page.title = "マラソン練習メニュー生成"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO

    # マラソンメニュー生成器のインスタンス
    menu_generator = MarathonMenuGenerator()

    # 入力フィールド
    target_time = ft.TextField(
        label="目標タイム (例: 3:30:00)",
        hint_text="時:分:秒の形式で入力",
        width=200
    )

    target_months = ft.TextField(
        label="何ヶ月後",
        hint_text="例: 6",
        width=150,
        keyboard_type=ft.KeyboardType.NUMBER
    )


    def generate_menu(e):
        # ロジッククラスを使用してメニュー生成処理を実行
        result_text, is_success = menu_generator.generate_menu(
            target_time.value,
            target_months.value
        )

        # UI更新
        menu_container.content = ft.Text(
            result_text,
            size=14,
            selectable=True,
            color=ft.Colors.RED if not is_success else None
        )

        page.update()

    # 生成ボタン
    generate_button = ft.ElevatedButton(
        text="練習メニューを生成",
        on_click=generate_menu,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE
        )
    )

    # 練習メニュー表示エリア
    menu_container = ft.Container(
        content=ft.Text("練習メニューがここに表示されます", size=16),
        bgcolor=ft.Colors.BLUE_GREY_50,
        padding=20,
        margin=ft.margin.only(top=20),
        border_radius=10,
        width=600
    )

    # レイアウト
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("🏃‍♂️ マラソン練習メニュー生成", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Row([
                    target_time,
                    target_months
                ], alignment=ft.MainAxisAlignment.START),
                generate_button,
                menu_container
            ], spacing=20),
            padding=30,
            alignment=ft.alignment.top_center
        )
    )


ft.app(main)
