import json
from decimal import Decimal
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder

def make_gauge(
    *,
    value: float,
    title: str,
    ranges: list[tuple[float, float, str]],
    max_value: float,
):
    return go.Figure(
        data=[
            go.Indicator(
                mode="gauge+number",
                value=value,
                title={"text": title},
                gauge={
                    "axis": {"range": [0, max_value]},
                    "steps": [
                        {"range": [r[0], r[1]], "color": r[2]}
                        for r in ranges
                    ],
                },
            )
        ]
    )

def make_forecast_charts(forecast):
    nitrate = float(forecast.nitrate_ppm)
    phosphate = float(forecast.phosphate_ppm)
    organic = float(forecast.organic_load_index)

    fig_nitrate = make_gauge(
        value=nitrate,
        title="Нитраты (NO₃, ppm)",
        ranges=[
            (0, 20, "#dff0d8"),   # хорошо
            (20, 40, "#fcf8e3"), # допустимо
            (40, 80, "#f2dede"), # плохо
        ],
        max_value=max(80, nitrate * 1.2),
    )
    fig_nitrate.update_layout(height=300)

    fig_phosphate = make_gauge(
        value=phosphate,
        title="Фосфаты (PO₄, ppm)",
        ranges=[
            (0, 0.2, "#dff0d8"),   # хорошо
            (0.2, 0.5, "#fcf8e3"), # допустимо
            (0.5, 1.0, "#f2dede"), # плохо
        ],
        max_value=max(1.0, phosphate * 1.2),
    )
    fig_phosphate.update_layout(height=300)

    fig_organic = make_gauge(
        value=organic,
        title="Индекс органической нагрузки",
        ranges=[
            (0, 1, "#dff0d8"),
            (1, 2, "#fcf8e3"),
            (2, 3, "#f2dede"),
        ],
        max_value=max(3.0, organic * 1.2),
    )
    fig_organic.update_layout(height=300)

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
        name="Индекс органической нагрузки",
        yaxis="y2"
    ))

    fig.update_layout(
        title="30‑дневный прогноз качества воды",
        xaxis_title="День",
        yaxis_title="Концентрация (ppm)",
        yaxis2=dict(
            title="Индекс органической нагрузки",
            overlaying="y",
            side="right"
        ),
        template="plotly_white",
        height=420,
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(orientation="h"),
    )

    return json.dumps(fig, cls=PlotlyJSONEncoder)