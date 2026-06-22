from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html


DATA_DIR = Path("data")

# Official Quantium processed file
OFFICIAL_FILE = DATA_DIR / "processed_data.csv"

# Your custom processed file
CUSTOM_FILE = DATA_DIR / "processed_custom_sales.csv"

if OFFICIAL_FILE.exists():
    DATA_FILE = OFFICIAL_FILE
else:
    DATA_FILE = CUSTOM_FILE


def load_data():
    df = pd.read_csv(DATA_FILE)

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
    df["Region"] = df["Region"].astype(str).str.lower().str.strip()

    df = df.dropna(subset=["Date", "Sales"])
    df = df.sort_values("Date")

    return df


sales_data = load_data()


def create_sales_chart(selected_region):
    if selected_region != "all":
        filtered_df = sales_data[sales_data["Region"] == selected_region]
    else:
        filtered_df = sales_data.copy()

    daily_sales = (
        filtered_df.groupby("Date", as_index=False)["Sales"]
        .sum()
        .sort_values("Date")
    )

    title_region = selected_region.title() if selected_region != "all" else "All Regions"

    fig = px.line(
        daily_sales,
        x="Date",
        y="Sales",
        markers=True,
        title=f"Sales Over Time - {title_region}",
        labels={
            "Date": "Date",
            "Sales": "Total Sales",
        },
    )

    fig.update_layout(
        title={
            "x": 0.5,
            "xanchor": "center",
            "font": {
                "size": 24,
                "family": "Arial",
            },
        },
        plot_bgcolor="white",
        paper_bgcolor="white",
        font={
            "family": "Arial",
            "size": 14,
            "color": "#263238",
        },
        xaxis={
            "title": "Date",
            "showgrid": True,
            "gridcolor": "#E0E0E0",
        },
        yaxis={
            "title": "Total Sales",
            "showgrid": True,
            "gridcolor": "#E0E0E0",
        },
        margin={
            "l": 60,
            "r": 40,
            "t": 80,
            "b": 60,
        },
    )

    fig.update_traces(
        line={
            "width": 3,
            "color": "#E91E63",
        },
        marker={
            "size": 6,
            "color": "#880E4F",
        },
    )

    price_increase_date = pd.Timestamp("2021-01-15")

    if not daily_sales.empty:
        min_date = daily_sales["Date"].min()
        max_date = daily_sales["Date"].max()

        if min_date <= price_increase_date <= max_date:
            fig.add_vline(
                x=price_increase_date,
                line_width=2,
                line_dash="dash",
                line_color="#212121",
                annotation_text="Price increase",
                annotation_position="top left",
            )

    return fig


app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    "Soul Foods Pink Morsels Sales Visualiser",
                    style={
                        "textAlign": "center",
                        "color": "#FFFFFF",
                        "fontFamily": "Arial",
                        "fontSize": "36px",
                        "marginBottom": "10px",
                    },
                ),
                html.P(
                    "Explore sales trends by region and understand whether sales changed after the price increase.",
                    style={
                        "textAlign": "center",
                        "color": "#FCE4EC",
                        "fontFamily": "Arial",
                        "fontSize": "18px",
                        "marginTop": "0",
                    },
                ),
            ],
            style={
                "background": "linear-gradient(135deg, #AD1457, #E91E63)",
                "padding": "35px",
                "borderRadius": "18px",
                "boxShadow": "0 6px 18px rgba(0,0,0,0.18)",
                "marginBottom": "30px",
            },
        ),

        html.Div(
            children=[
                html.H3(
                    "Filter sales by region",
                    style={
                        "fontFamily": "Arial",
                        "color": "#AD1457",
                        "marginBottom": "15px",
                    },
                ),

                dcc.RadioItems(
                    id="region-radio",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "East", "value": "east"},
                        {"label": "South", "value": "south"},
                        {"label": "West", "value": "west"},
                    ],
                    value="all",
                    inline=True,
                    style={
                        "fontFamily": "Arial",
                        "fontSize": "17px",
                        "color": "#263238",
                    },
                    labelStyle={
                        "display": "inline-block",
                        "marginRight": "25px",
                        "padding": "10px 16px",
                        "border": "1px solid #F8BBD0",
                        "borderRadius": "20px",
                        "backgroundColor": "#FCE4EC",
                        "cursor": "pointer",
                    },
                ),
            ],
            style={
                "backgroundColor": "#FFFFFF",
                "padding": "25px",
                "borderRadius": "16px",
                "boxShadow": "0 4px 14px rgba(0,0,0,0.10)",
                "marginBottom": "30px",
            },
        ),

        html.Div(
            children=[
                dcc.Graph(
                    id="sales-line-chart",
                    figure=create_sales_chart("all"),
                    style={
                        "height": "620px",
                    },
                ),
            ],
            style={
                "backgroundColor": "#FFFFFF",
                "padding": "25px",
                "borderRadius": "16px",
                "boxShadow": "0 4px 14px rgba(0,0,0,0.10)",
            },
        ),
    ],
    style={
        "backgroundColor": "#F7F7F7",
        "minHeight": "100vh",
        "padding": "35px",
    },
)


@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-radio", "value"),
)
def update_chart(selected_region):
    return create_sales_chart(selected_region)


if __name__ == "__main__":
    app.run(debug=True)