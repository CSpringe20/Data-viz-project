import pandas as pd
import numpy as np
import plotly.express as px

# load data
data = pd.read_csv("../dataset/weatherAUS.csv")
cities = pd.read_csv("../dataset/cities.csv")

# vars
min_date = "2009-01-01" # some cities have data for 2008 too but not all so we cut to 2009
max_date = "2017-06-25" # every city has data to this day
banned_cities = ['Dartmoor','Katherine','Nhil','Uluru'] # coz their data starts in 2013 and i dont wanna bother

# consider only certain cities and years
data = data[~data["Location"].isin(banned_cities)]

# first one is group by month, second is group by year, select one
data["Date"] = data["Date"].str[:-2] + "01"
#data["Date"] = data["Date"].str[:-5] + "01-01"

data["Date"] = pd.to_datetime(data["Date"])
data = data[data["Date"]>=min_date]
data = data[data["Date"]<=max_date]

# create mean and variance of temperature for each city and day
data["Mean"] = (data["MaxTemp"]+ data["MinTemp"] + data["Temp9am"] + data["Temp3pm"]) / 4
data["Variance"] = data["MaxTemp"] - data["MinTemp"]

# groupby location and month
groupby = data.groupby(['Location','Date'])

out = pd.DataFrame({
    'avgMinTemp': groupby['MinTemp'].mean(),
    'avgTemp9am': groupby['Temp9am'].mean(),
    'avgTemp3pm': groupby['Temp3pm'].mean(),
    'avgMaxTemp': groupby['MaxTemp'].mean(),
    'avgTempMean': groupby['Mean'].mean(),
    'avgTempVar': groupby['Variance'].mean()
})
out = out.reset_index()  # brings 'Location' and 'Date' back as columns

# select the variables you want to plot from the ones in "out"
var1 = "avgTempMean"
var2 = "avgTempVar"

# select the cool cities and their color
cpt = cities[cities["Representative"]==1]
capitals = np.array(cpt["Location"])
colors = ["red",
          "blue",
          "green",
          "yellow",
          "purple"]
pos = ["bot",  # not used but these are the location of colored cities
       "mid",
       "right",
       "top",
       "left"]
       
highlight_cities = {city: color for city, color in zip(capitals, colors)}

# assign all other cities to black
all_locations = out["Location"].unique()
color_map = {loc: highlight_cities.get(loc, "black") for loc in all_locations}

fig = px.scatter(
    out,
    x=var1,
    y=var2,
    animation_frame=out["Date"].dt.strftime("%Y-%m"), # show just year instead of entire timestamp
    animation_group="Location",
    color="Location",
    color_discrete_map=color_map
)

for trace in fig.data:
    if trace.name in capitals:  # highlighted cities
        trace.showlegend = True
        trace.marker.update(size=48)   # bigger colored dots
    else:
        trace.showlegend = False
        trace.marker.update(size=12)    # smaller black dots

fig.update_layout(
    legend=dict(font=dict(size=22)), # adjust legend

    title=dict(                      # adjust title
        text="<b>SEASONAL CHANGES IN AUSTRALIA</b>",
        font=dict(size=42)),

    title_x=0.5,  # make title centered
    xaxis=dict(   # adjust x axis
        title=dict(text="MEAN (°C)", font=dict(size=38)),
        tickfont=dict(size=28)),

    yaxis=dict(   # adjust y axis
        title=dict(text="VARIANCE (°C)", font=dict(size=38)),
        tickfont=dict(size=28))
)
fig.layout.sliders[0].font = dict(size=28)  # adjust thing at the bottom

# adjust speed and axes
speed = 500
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = speed  # 1s per frame
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = speed  # smooth transition

fig.update_xaxes(range=[out[var1].min()*0.95, out[var1].max()*1.05])
fig.update_yaxes(range=[out[var2].min()*0.95, out[var2].max()*1.05])
fig.write_html("../images/viz1.html")
fig.show()