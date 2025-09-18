import flet as ft  # type: ignore


def main(page: ft.Page):
    def calculate(e):
        num1 = int(num1_input.value)
        num2 = int(num2_input.value)

        result = num1 + num2
        result_text.value = f"結果: {num1} + {num2} = {result}"
        result_text.update()

    num1_input = ft.TextField(label="数値1", value="1", on_change=calculate)
    num2_input = ft.TextField(label="数値2", value="3", on_change=calculate)
    result_text = ft.Text("結果: -", size=20)

    page.add(
        ft.Column(
            [
                num1_input,
                num2_input,
                result_text,
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True,
        )
    )


ft.app(main)
