import datetime as dt

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

DATA_PATH = "data/pink_morsel_sales.csv"  # adjust if your filename differs
MARKER_DATE = dt.datetime(2021, 1, 15)

# Load + prep once
df = pd.read_csv(DATA_PATH)
df["Date"] = pd.to_datetime(df["Date"])
df["Region"] = df["Region"].astype(str).str.strip().str.lower()
df = df.sort_values("Date")

REGION_OPTIONS = ["all", "north", "east", "south", "west"]

app = Dash(__name__)
app.title = "Pink Morsel Sales"

app.layout = html.Div(
    className="page",
    children=[
        html.Div(
            className="card header",
            children=[
                html.H1("Pink Morsel Sales Visualiser", className="title"),
                html.P(
                    "Use the filter to explore region-specific sales. "
                    "The dashed line marks the price increase on 2021-01-15.",
                    className="subtitle",
                ),
            ],
        ),
        html.Div(
            className="card controls",
            children=[
                html.Label("Filter by region", className="label"),
                dcc.RadioItems(
                    id="region-filter",
                    options=[{"label": r.title(), "value": r} for r in REGION_OPTIONS],
                    value="all",
                    inline=True,
                    className="radio",
                ),
            ],
        ),
        html.Div(
            className="card chart",
            children=[
                dcc.Graph(id="sales-line-chart", config={"displayModeBar": False}),
            ],
        ),
        html.Div(
            className="footer",
            children="Tip: Select 'All' to compare overall sales before vs after the price increase.",
        ),
    ],
)


@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-filter", "value"),
)
def update_chart(region: str):
    if region == "all":
        filtered = df.copy()
        title_region = "All Regions"
    else:
        filtered = df[df["Region"] == region]
        title_region = region.title()

    daily = filtered.groupby("Date", as_index=False)["Sales"].sum()

    fig = px.line(
        daily,
        x="Date",
        y="Sales",
        title=f"Pink Morsel Total Daily Sales — {title_region}",
        labels={"Date": "Date", "Sales": "Total Sales"},
    )

    # Price increase marker
    fig.add_vline(x=MARKER_DATE, line_dash="dash")
    if not daily.empty:
        fig.add_annotation(
            x=MARKER_DATE,
            y=float(daily["Sales"].max()),
            text="Price increase (2021-01-15)",
            showarrow=False,
            yanchor="bottom",
        )

    fig.update_layout(
        margin=dict(l=30, r=30, t=60, b=30),
        hovermode="x unified",
    )
    return fig


if __name__ == "__main__":
    app.run(debug=True)