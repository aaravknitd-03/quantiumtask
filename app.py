from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html


DATA_DIR = Path("data")

# Use official processed file if available.
# Otherwise use your custom processed file.
OFFICIAL_FILE = DATA_DIR / "processed_data.csv"
CUSTOM_FILE = DATA_DIR / "processed_custom_sales.csv"

if OFFICIAL_FILE.exists():
    DATA_FILE = OFFICIAL_FILE
else:
    DATA_FILE = CUSTOM_FILE


def load_data():
    df = pd.read_csv(DATA_FILE)

    # Make sure Date is treated as an actual date
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Remove bad rows if any
    df = df.dropna(subset=["Date", "Sales"])

    # Sort by date
    df = df.sort_values("Date")

    # Combine sales for the same date
    daily_sales = (
        df.groupby("Date", as_index=False)["Sales"]
        .sum()
        .sort_values("Date")
    )

    return daily_sales


sales_data = load_data()

fig = px.line(
    sales_data,
    x="Date",
    y="Sales",
    title="Sales Over Time",
    labels={
        "Date": "Date",
        "Sales": "Total Sales",
    },
)

fig.update_layout(
    title_x=0.5,
    xaxis_title="Date",
    yaxis_title="Total Sales",
)


app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(
            "Soul Foods Sales Visualiser",
            style={
                "textAlign": "center",
                "fontFamily": "Arial",
                "marginTop": "30px",
            },
        ),
        html.P(
            "Line chart showing sales over time to understand whether sales were higher before or after the price increase.",
            style={
                "textAlign": "center",
                "fontFamily": "Arial",
                "fontSize": "18px",
            },
        ),
        dcc.Graph(
            id="sales-line-chart",
            figure=fig,
        ),
    ],
    style={
        "width": "90%",
        "margin": "auto",
    },
)

if __name__ == "__main__":
    app.run(debug=True)