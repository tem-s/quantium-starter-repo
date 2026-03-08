import pandas as pd
import datetime as dt
from dash import Dash, dcc, html
import plotly.express as px


DATA_PATH = "data/pink_morsel_sales.csv"  # change if your file name differs
PRICE_INCREASE_DATE = "2021-01-15"

# Load and prepare data
df = pd.read_csv(DATA_PATH)

# Ensure correct types + sort
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# Total sales per day (across all regions)
daily = df.groupby("Date", as_index=False)["Sales"].sum()

# Build chart
fig = px.line(
    daily,
    x="Date",
    y="Sales",
    title="Pink Morsel Sales Over Time",
    labels={"Date": "Date", "Sales": "Total Sales"},
)

marker_date = dt.datetime(2021, 1, 15)

fig.add_vline(x=marker_date, line_dash="dash")

fig.add_annotation(
    x="2021-01-15",
    y=daily["Sales"].max(),
    text="Price increase (2021-01-15)",
    showarrow=False,
    yanchor="bottom",
)

app = Dash(__name__)

app.layout = html.Div(
    style={"maxWidth": "1100px", "margin": "0 auto", "padding": "24px"},
    children=[
        html.H1("Pink Morsel Sales Visualiser"),
        html.P(
            "This chart shows total daily sales for Pink Morsels. "
            "The dashed line marks the price increase on 2021-01-15."
        ),
        dcc.Graph(figure=fig),
    ],
)

if __name__ == "__main__":
    app.run(debug=True)