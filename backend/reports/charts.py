from openpyxl.chart import PieChart, Reference
from openpyxl.chart.layout import Layout, ManualLayout


def generate_percentage_band_chart(ws, bands, row):

    # Write data hidden
    start = row + 5
    data = [
        ("90+", bands["90%+"]),
        ("80-89", bands["80-89%"]),
        ("70-79", bands["70-79%"]),
        ("60-69", bands["60-69%"]),
        ("<60", bands["<60%"])
    ]

    r = start
    for label, val in data:
        ws[f"Z{r}"] = label
        ws[f"AA{r}"] = val
        r += 1

    pie = PieChart()
    pie.title = "Percentage Distribution"

    # 🔥 PUSH PIE DOWN INSIDE CHART
    pie.layout = Layout(
        manualLayout=ManualLayout(
            y=0.15,   # move plot area down
            h=0.8     # reduce height slightly
        )
    )

    values = Reference(ws, min_col=27, min_row=start, max_row=r-1)
    labels = Reference(ws, min_col=26, min_row=start, max_row=r-1)

    pie.add_data(values)
    pie.set_categories(labels)

    # place chart
    ws.add_chart(pie, f"E{row}")
