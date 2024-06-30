import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import geopandas as gpd
import numpy as np
from pretty_html_table import build_table

st.title("Soil Properties with Marked Coordinates for Orissa")

@st.cache_resource
def load_data():
    df1 = pd.read_csv('edited_Table1.csv', index_col=0)
    temp_df = df1.copy()
    temp_df = temp_df[['lat_long','x','y']]
    temp_df.drop_duplicates(inplace=True)
    coords = [{'x': row['x'], 'y': row['y']} for index, row in temp_df.iterrows()]
    return coords, df1

@st.cache_resource
def main():
    # Load data
    coordinates, df1 = load_data()

    # Create a Folium map centered around the first location
    map_center = (np.mean([coord['x'] for coord in coordinates]), np.mean([coord['y'] for coord in coordinates]))
    m = folium.Map(location=map_center, zoom_start=5)

    # Add district layer
    gdf = gpd.read_file('odisha.geojson')
    for _, row in gdf.iterrows():
        temp_poly = row['geometry']
        folium.GeoJson(temp_poly).add_to(m)

    # Add markers to the map with popups
    for coord in coordinates:
        filtered_df = df1[(df1['x'] == coord['x']) & (df1['y'] == coord['y'])]
        if not filtered_df.empty:
            html = filtered_df.iloc[:,:9].to_html(classes="table table-striped table-hover table-condensed table-responsive")
            popup = folium.Popup(html)
            folium.Marker(
                location=(coord["x"], coord["y"]),
                tooltip=str(coord['x']) + ' , ' + str(coord['y']),
                popup=popup
            ).add_to(m)

    return m

# Render the map
if 'map' not in st.session_state:
    st.session_state['map'] = main()

folium_static(st.session_state['map'], width=800, height=500)

# Add inputs and table display
col1, col2 = st.columns(2)
with col1:
    x = float(st.text_input("Latitude: ", value=0))
    y = float(st.text_input("Longitude: ", value=0))

# Filter and display table
df1 = load_data()[1]  # Reload the DataFrame
x_check = np.isclose(df1.x, x)
y_check = np.isclose(df1.y, y)
filtered_df = df1[np.logical_and(x_check, y_check)]
st.table(filtered_df)

# Download button for filtered data
st.download_button(
    "Download data in CSV format",
    filtered_df.to_csv().encode("utf-8"),
    file_name=f"Data_Table1_{x}_{y}.csv",
    mime="text/csv"
)
