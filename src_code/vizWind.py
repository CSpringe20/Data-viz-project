import pandas as pd, numpy as np, plotly.express as px

df = pd.read_csv("../dataset/weatherAUS.csv")

time = "9am"

compass_order = [
    "N","NNE","NE","ENE","E","ESE","SE","SSE",
    "S","SSW","SW","WSW","W","WNW","NW","NNW"
]
df[f"WindDir{time}"] = pd.Categorical(df[f"WindDir{time}"], categories=compass_order, ordered=True)

speed_bins   = [0, 5, 10, 15, 20, 1000]
speed_labels = ["0–5","5–10","10–15","15–20","20+"]
df["Wind speed"] = pd.cut(df[f"WindSpeed{time}"], bins=speed_bins, labels=speed_labels, include_lowest=True)

counts = (df.groupby([f"WindDir{time}", "Wind speed"])
            .size()
            .reset_index(name="count"))

# keep only strong winds and create a safe copy
strong_counts = counts[counts["Wind speed"] == "20+"].copy()

threshold = 2100
strong_counts["low_high"] = np.where(
    strong_counts["count"] < threshold, "Below threshold", "Above threshold"
)

fig = px.bar_polar(
    strong_counts,
    r="count",
    theta=f"WindDir{time}",
    color="low_high",  # <- use the new column for coloring
    category_orders={"low_high": ["Below threshold", "Above threshold"]},
    color_discrete_map={
        "Below threshold": "lightgrey",
        "Above threshold": "red"
    },
    title=""
)

fig.update_layout(
    polar=dict(
        angularaxis=dict(direction="clockwise", rotation=68, tickfont=dict(size=22)),
        radialaxis=dict(showticklabels=False, showline=False, ticks='')
    ),
    showlegend=False
)

fig.show()
