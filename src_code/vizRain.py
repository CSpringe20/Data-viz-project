import numpy as np, pandas as pd, geopandas as gpd
import plotly.express as px

# import data
data = pd.read_csv("../dataset/weatherAUS.csv", parse_dates=['Date'])
cities = pd.read_csv("../dataset/cities.csv")
season = "summer"
data = data[data['Rainfall'].notna()]

if season == "summer":
    # October–March (warm half)
    data = data[(data['Date'].dt.month >= 10) | (data['Date'].dt.month < 4)]
else:
    # April–September (cool half)
    data = data[(data['Date'].dt.month >= 4) & (data['Date'].dt.month < 10)]

# average across location (1 data for each city)
groupby = data.groupby(['Location'])

out = pd.DataFrame({
    'avgRainfall': groupby['Rainfall'].mean()
})
out = out.reset_index() 
out = out.merge(cities[['Location','Latitude','Longitude']], on='Location', how='left')

d = out[["avgRainfall","Latitude","Longitude"]].copy() # for Rainfall
#d = cities # for Population

fig = px.density_mapbox(
    d,
    lat="Latitude",
    lon="Longitude",
    z="avgRainfall",  # avgRainfall / Population 
    radius=100,                     
    center=dict(lat=-25, lon=133),  # center on Australia
    zoom=4.0,
    mapbox_style="carto-positron", # open-street-map / carto-positron
    color_continuous_scale="Blues", # Blues for rainfall / OrRd for population
)

fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    coloraxis_colorbar=dict(title="")
)

fig.show()
