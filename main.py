import streamlit as st
import folium
from streamlit_folium import st_folium,folium_static
import pandas as pd
import geopandas as gpd

@st.cache_resource
def load_data():
    df1 = pd.read_csv('edited_Table1.csv',index_col=0)
    coords = [{'x':row['x'],'y':row['y']} for index,row in df1.iterrows()]
    return coords,df1

st.title("Soil Properties with Marked Coordinates for Orissa")

@st.cache_resource
def main():

    # Define coordinates
    coordinates,df1 = load_data()
    print(len(coordinates),df1.shape)

    # Create a Folium map centered around the first location
    cent_X = 0
    cent_Y = 0
    for coords in coordinates:
        cent_X+=coords['x']
        cent_Y+=coords['y']
    cent_X = cent_X/len(coordinates)
    cent_Y = cent_Y/len(coordinates)
    map_center = (cent_X, cent_Y)
    m = folium.Map(location=map_center, zoom_start=5)

    # Add district layer
    gdf = gpd.read_file('odisha.geojson')
    for index,row in gdf.iterrows():
        temp_poly = row['geometry']
        folium.GeoJson(temp_poly).add_to(m)


    # Add markers to the map
    for coord in coordinates:
        temp_df = pd.DataFrame(df1[df1['x']==coord['x']][df1['y']==coord['y']])
        html = temp_df.iloc[:,0:9].to_html(
                classes="table table-striped table-hover table-condensed table-responsive"
            )
        popup = folium.Popup(html, max_width=500)
        folium.Marker(
            location=(coord["x"], coord["y"]),
            tooltip = str(coord['x']) + ' , ' + str(coord['y']),
            popup = popup
        ).add_to(m)

    # Display the map in Streamlit
    return m

load_data()
if 'map' not in st.session_state:
    map = main()
    st.session_state['map'] = map
data = st_folium(st.session_state['map'], width=800, height=500)
st.write(data)

