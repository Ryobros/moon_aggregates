import pandas as pd
import folium
from folium.plugins import MarkerCluster
import os

# Load CSV data
def satVis(csv_path:str,
           sep:str=";"):
    df = pd.read_csv(csv_path, sep=sep)
    df.columns = df.columns.str.strip()

# Direct map visual centered berdasarkan rata rata koordinat
    center_lat = df["latitude"].mean()
    center_lon = df["longitude"].mean()

    # Membuat Folium map bernuansa satelit
    m = folium.Map(location=[center_lat, center_lon], zoom_start=15, tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri')

    # Add markers for each point
    marker_cluster = MarkerCluster().add_to(m)

    for idx, row in df.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"Point {idx+1}: ({row['latitude']:.6f}, {row['longitude']:.6f})",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(marker_cluster)

    # Save

    output_dir = '../data/output/map/'
    output_file = os.path.join(output_dir, 'satellite_visualization.html')

    # PROTEKSI
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Folder {output_dir} berhasil dibuat.")
    
    m.save('../data/output/map/satellite_visualization.html')
    print("Map saved as 'satellite_visualization.html'. Open it in a web browser to view.")



