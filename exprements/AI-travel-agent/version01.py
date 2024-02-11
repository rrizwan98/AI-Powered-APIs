# Import libraries
import plotly.express as px
import pandas as pd

# token = "pk.eyJ1IjoicmF6YS05OCIsImEiOiJjbHEzaWJkdjEwZHhsMnNseHdjcG5xM2x5In0.YJhEoq8E7Rdne1fSidrfBQ" # you will need your own token
# px.set_mapbox_access_token(token)

# Read the data from a CSV file
locations = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv", # provide the file name of your dataset
    # names=["country_code", "lat", "lon", "country", "usa_state_code", "usa_state_lat", "usa_state_lon", "usa_state"], # provide the column names of your dataset
    # names = ["country", "city","accentCity","region","population","lat", "lon"]
    names = ["city", "state","population","lat", "lon"]
)
locations = locations.drop(0)
print(locations.head(10))

# Ask the user where they want to go
user_input = input("Where do you want to go in these locations? ")

# Filter the data frame based on the user's input
filtered_locations = locations.query("city == @user_input")

# Create a world map with the selected location as a point
fig = px.scatter_mapbox(
    filtered_locations,
    lat="lat",
    lon="lon",
    hover_name="city",
    color_discrete_sequence=["fuchsia"],
    showsubunits=True, subunitcolor="Blue",
    zoom=15,
    height=500,
    center={"lat": float(filtered_locations["lat"].iloc[0]), "lon": float(filtered_locations["lon"].iloc[0])}
)

# Update the layout of the map
fig.update_layout(
    mapbox_style="open-street-map", # you can change the style of the map
    # mapbox_style="light", # you can change the style of the map
    margin={"r":0,"t":0,"l":0,"b":0}
)

# Show the map
fig.write_html('map.html', auto_open=True)
# fig.show()

#https://plotly.com/python/maps/