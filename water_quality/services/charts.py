import json
from decimal import Decimal
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder

def make_forecast_charts(forecast):
    nitrate = float(forecast.nitrate_ppm)
    phosphate = float(forecast.phosphate_ppm)
    organic = float(forecast.organic_load_index)

    fig_nitrate = go.Figure(data=[go.Bar(x=["NO3"], y=[nitrate])])
    fig_nitrate.update_layout(
        title="Nitrate (ppm)",
        yaxis_title="ppm",
        height=300,
        margin=dict(l=30, r=30, t=50, b=30),
    )

    fig_phosphate = go.Figure(
        data=[go.Bar(x=["PO4"], y=[phosphate])]
    )
    fig_phosphate.update_layout(
        title="Phosphate (ppm)",
        yaxis_title="ppm",
        height=300,
        margin=dict(l=30, r=30, t=50, b=30),
    )

    fig_organic = go.Figure(
        data=[
            go.Indicator(
                mode="gauge+number",
                value=organic,
                title={"text": "Organic load index"},
                gauge={
                    "axis": {"range": [0, max(3.0, organic * 1.2)]},
                    "steps": [
                        {"range": [0, 1], "color": "#dff0d8"},
                        {"range": [1, 2], "color": "#fcf8e3"},
                        {"range": [2, 3], "color": "#f2dede"},
                    ],
                },
            )
        ]
    )
    fig_organic.update_layout(
        height=300,
        margin=dict(l=30, r=30, t=50, b=30),
    )

    return {
        "nitrate_json": json.dumps(fig_nitrate, cls=PlotlyJSONEncoder),
        "phosphate_json": json.dumps(fig_phosphate, cls=PlotlyJSONEncoder),
        "organic_json": json.dumps(fig_organic, cls=PlotlyJSONEncoder),
    }

def make_daily_forecast_charts(rows):
    days = [r["day"] for r in rows]
    no3 = [r["no3"] for r in rows]
    po4 = [r["po4"] for r in rows]
    organic = [r["organic"] for r in rows]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=days, y=no3,
        mode="lines+markers",
        name="NO₃ (ppm)"
    ))

    fig.add_trace(go.Scatter(
        x=days, y=po4,
        mode="lines+markers",
        name="PO₄ (ppm)"
    ))

    fig.add_trace(go.Scatter(
        x=days, y=organic,
        mode="lines+markers",
        name="Organic load index",
        yaxis="y2"
    ))

    fig.update_layout(
        title="30‑day water quality forecast",
        xaxis_title="Day",
        yaxis_title="ppm",
        yaxis2=dict(
            title="Organic load index",
            overlaying="y",
            side="right"
        ),
        template="plotly_white",
        height=420,
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(orientation="h"),
    )

    return json.dumps(fig, cls=PlotlyJSONEncoder)