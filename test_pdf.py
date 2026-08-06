from pathlib import Path

from utils.pdf_report_generator import generate_pdf_report


class MockMemory:

    def __init__(self):

        self.report_text = Path(
            "outputs/report.md"
        ).read_text(
            encoding="utf-8"
        )

        self.analysis = {

            "visualizations": {

                "line_Timestamp_total_bytes":
                    "outputs/charts/Timestamp_total_bytes_line.png",

                "pie_action":
                    "outputs/charts/action_pie.png",

                "bar_app_category_total_bytes":
                    "outputs/charts/app_category_total_bytes_bar.png",

                "bar_src_country_total_bytes":
                    "outputs/charts/src_country_total_bytes_bar.png",

                "scatter_bytes_sent_bytes_received":
                    "outputs/charts/bytes_sent_bytes_received_scatter.png",
            },

            "profile": {

                "rows": 84550,
                "columns": 61,
                "duplicate_rows": 42225,
            },
        }

    def get_report(self, fmt):
        return self.report_text

    def get_analysis(self, key):
        return self.analysis.get(key)


memory = MockMemory()

pdf = generate_pdf_report(
    memory,
    output_pdf="outputs/test_pdf.pdf",
)

print(f"PDF generated: {pdf}")