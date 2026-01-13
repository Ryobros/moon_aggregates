import pandas as pd
import folium
from folium.plugins import MarkerCluster

# Load CSV data
def satVis(csv_path:str,
           sep:str=","):
    df = pd.read_csv('csv_path')

# Create a map centered on the mean coordinates
    center_lat = df['latitude'].mean()
    center_lon = df['longitude'].mean()

    # Create a Folium map with satellite tiles
    m = folium.Map(location=[center_lat, center_lon], zoom_start=15, tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri')

    # Add markers for each point
    marker_cluster = MarkerCluster().add_to(m)

    for idx, row in df.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"Point {idx+1}: ({row['latitude']:.6f}, {row['longitude']:.6f})",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(marker_cluster)

    # Save the map
    m.save('../data/output/map/satellite_visualization.html')
    print("Map saved as 'satellite_visualization.html'. Open it in a web browser to view.")



