import flet as ft

import polars as pl
import io


def main(page: ft.Page):
    page.title = "CSV Data Visualizer with Flet BarChart"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 1000
    page.window_height = 5000
    page.scroll = ft.ScrollMode.ALWAYS

    df = None  # Polars DataFrame を保持する変数

    # ダミーCSVデータの準備
    dummy_csv_data = """Category,Value,Another_Value
A,10,5
B,15,8
C,7,12
D,20,3
E,12,10
"""

    # グラフ表示用のコンテナ
    chart_container = ft.Container(
        width=800,
        height=800,
        content=ft.Text(
            "Upload a CSV to see the chart.", text_align=ft.TextAlign.CENTER
        ),
        # alignment=ft.alignment.center(),
        border=ft.border.all(1, ft.Colors.BLUE_GREY_200),
        border_radius=ft.border_radius.all(5),
        visible=False,
    )

    csv_input_textfield = ft.TextField(
        label="CSVデータをここに貼り付けてください (例: Category,Value,Another_Value\\nA,10,5)",
        multiline=True,
        min_lines=10,
        max_lines=20,
        width=600,
        hint_text="Category,Value,Another_Value\nA,10,5\nB,15,8",  # 例を表示
    )

    data_table_container = ft.Container(
        content=ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("No Data")),  # ダミーカラム
            ],
            rows=[],
            border=ft.border.all(1, ft.Colors.BLUE_GREY_100),
            vertical_lines=ft.BorderSide(1, ft.Colors.BLUE_GREY_100),
            horizontal_lines=ft.BorderSide(1, ft.Colors.BLUE_GREY_100),
            heading_row_color=ft.Colors.BLUE_GREY_50,
        ),
        visible=False,
        width=800,
        height=400,
        border=ft.border.all(1, ft.Colors.BLUE_GREY_200),
        border_radius=ft.border_radius.all(5),
        padding=ft.padding.all(10),
    )

    status_text = ft.Text("Load dummy data or upload a CSV file.", size=16)

    # グラフとテーブルを更新する関数
    def update_chart_and_table(data_frame: pl.DataFrame):
        nonlocal df
        df = data_frame

        if df is None or df.is_empty():
            chart_container.visible = False
            data_table_container.visible = False
            chart_container.content = ft.Text(
                "No data to display.", text_align=ft.TextAlign.CENTER
            )
            page.update()
            return

        table_control = data_table_container.content
        table_control.rows.clear()
        table_control.columns.clear()

        table_control.columns.extend(
            [ft.DataColumn(ft.Text(col)) for col in df.columns]
        )

        for row in df.head(5).iter_rows():
            table_control.rows.append(
                ft.DataRow([ft.DataCell(ft.Text(str(cell))) for cell in row])
            )

        # 棒グラフの描画
        if "Category" in df.columns and "Value" in df.columns:
            try:
                bar_groups = []
                for i, row_dict in enumerate(df.iter_rows(named=True)):
                    bar_groups.append(
                        ft.BarChartGroup(
                            x=i,  # x軸はカテゴリの順序インデックス
                            bar_rods=[
                                ft.BarChartRod(
                                    from_y=0,
                                    to_y=row_dict["Value"],  # 辞書からValue列の値を取得
                                    color=ft.Colors.BLUE_ACCENT_400,
                                    width=15,
                                )
                            ],
                        )
                    )

                bottom_titles = ft.ChartAxis(
                    labels=[
                        ft.ChartAxisLabel(
                            value=i, label=ft.Text(df["Category"].to_list()[i])
                        )
                        for i in range(len(df))
                    ],
                )

                max_value = int(df["Value"].max()) if not df["Value"].is_empty() else 0
                left_titles = ft.ChartAxis(
                    labels_interval=10,
                    labels=[
                        ft.ChartAxisLabel(value=i, label=ft.Text(str(i)))
                        for i in range(0, max_value + 10, 10)
                    ],
                )

                bar_chart = ft.BarChart(
                    bar_groups=bar_groups,
                    bottom_axis=bottom_titles,
                    left_axis=left_titles,
                    tooltip_bgcolor=ft.Colors.BLUE_GREY_700,
                    height=350,
                )

                chart_container.content = bar_chart
                chart_container.visible = True
                data_table_container.visible = True
                status_text.value = f"Data loaded and chart updated. Shape: {df.shape}"
            except Exception as e:
                status_text.value = f"Error creating chart: {e}. Make sure 'Category' and 'Value' columns exist."
                chart_container.visible = False
        else:
            chart_container.visible = False
            status_text.value = (
                "CSV must contain 'Category' and 'Value' columns for bar chart."
            )

        page.update()

    def process_csv_text(e):
        csv_text = csv_input_textfield.value
        if not csv_text:
            page.update()
            return

        try:
            df = pl.read_csv(io.StringIO(csv_text))
            update_chart_and_table(df)
        except Exception as ex:
            print(f"Error reading CSV data: {ex}")
        page.update()

    def load_dummy_data(e):
        nonlocal df
        new_df = pl.read_csv(io.BytesIO(dummy_csv_data.encode("utf-8")))
        update_chart_and_table(new_df)
        status_text.value = "Dummy data loaded successfully."
        page.update()

    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        csv_input_textfield,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Draw Chart",
                            icon=ft.Icons.BAR_CHART,
                            on_click=process_csv_text,
                        ),
                        # ft.ElevatedButton(
                        #     "Pick files",
                        #     icon=ft.Icons.UPLOAD_FILE,
                        #     on_click=lambda _: file_picker.pick_files(
                        #         allow_multiple=False
                        #     ),
                        # ),
                        ft.ElevatedButton(
                            "Load Dummy Data",
                            icon=ft.Icons.DATA_USAGE,
                            on_click=load_dummy_data,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                status_text,
                ft.Divider(),
                ft.Text("Bar Chart:", size=16),
                chart_container,
                ft.Divider(),
                ft.Text("First 5 Rows of Data:", size=16),
                data_table_container,
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )
    )


ft.app(main, view=ft.WEB_BROWSER)
