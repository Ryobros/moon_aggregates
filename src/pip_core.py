import geopandas as gpd
import pandas as pd
from pathlib import Path
import time


def pip_pipeline(
    shp_path: str,
    csv_path: str,
    polygon: str,
    output_dir: str,
    sep: str = ";",
    lon_col: str = "longitude",
    lat_col: str = "latitude"
):
    """
    Full PIP pipeline:
    1. load polygon kabupaten (kecamatan level)
    2. load point CSV
    3. points-in-polygon
    4. export CSV per kecamatan
    """

    # 1. Polygon administrasi
    print(f"Sedang memuat data polygon dari {shp_path}")
    polygons = load_polygon_admin(
        shp_path=shp_path,
        kabupaten=polygon
    )
    time.sleep(1)

    # 2. Titik
    print(f"Sedang memuat dataset dari {csv_path}")
    points = load_points_datasets(
        csv_path=csv_path,
        sep=sep,
        lon_col=lon_col,
        lat_col=lat_col,
        crs=polygons.crs
    )
    time.sleep(1)

    # 3. PIP
    print(f"Mohon tunggu......")
    pip_result = run_pip(
        points_gdf=points,
        polygon_gdf=polygons
    )

    # 4. Export
    export_by_kecamatan(
        pip_gdf=pip_result,
        output_dir=output_dir
    )
    time.sleep(1)
    print("Proses selesai")

    return pip_result


def load_polygon_admin(
        shp_path:str, 
        kabupaten:str 
) -> gpd.GeoDataFrame: 
    
    gdf = gpd.read_file(shp_path,
                        where=f"WADMKK = '{kabupaten}'"
                        )
    if gdf.empty:
        raise ValueError("Polygon Kosong")
    else:
        return gdf
    

def load_points_datasets(
            csv_path:str,
            sep:str = ';',
            lon_col:str = 'longitude', 
            lat_col:str = 'latitude',
            crs=None
    ) -> gpd.GeoDataFrame:
        
        df = pd.read_csv(csv_path, sep=sep)
        gdf = gpd.GeoDataFrame(
             df,  geometry=gpd.points_from_xy(df[lon_col], df[lat_col]),
        crs=crs
    )
        
        return gdf

def run_pip(points_gdf, polygon_gdf):
    if points_gdf.crs != polygon_gdf.crs:
        points_gdf = points_gdf.to_crs(polygon_gdf.crs)
    pip = gpd.sjoin(
         points_gdf,
         polygon_gdf[["WADMKC", "WADMKD", "geometry"]],
         how="inner",
         predicate="within"
    )
    return pip


def export_by_kecamatan(pip_gdf, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for kec, group in pip_gdf.groupby("WADMKC"):
        if pd.isna(kec):
            continue

        fname = f"kecamatan_{kec.lower().replace(' ', '_')}.csv"
        group.drop(columns="geometry").to_csv(output_dir / fname, index=False)






