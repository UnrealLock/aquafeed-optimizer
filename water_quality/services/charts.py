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