import pandas as pd
import re
from pathlib import Path

def parse_coord(coord_str):
    """
    Parse koordinat format 'S6.96593 E107.75441' menjadi (-6.96593, 107.75441)
    """
    if pd.isna(coord_str) or not isinstance(coord_str, str):
        return None, None
    
    # Pattern untuk menangkap N/S dan E/W dengan angka desimal
    pattern = r'([NS])\s*(-?\d+\.?\d*)\s+([EW])\s*(-?\d+\.?\d*)'
    match = re.search(pattern, coord_str.strip())
    
    if not match:
        return None, None
    
    lat_dir, lat_val, lon_dir, lon_val = match.groups()
    
    # Konversi ke float
    lat = float(lat_val)
    lon = float(lon_val)
    
    # Aplikasikan tanda negatif untuk S dan W
    if lat_dir == 'S':
        lat = -lat
    if lon_dir == 'W':
        lon = -lon
    
    return lat, lon

def detect_coordinate_columns(df):
    """
    Deteksi kolom yang kemungkinan berisi koordinat
    """
    coord_columns = []
    
    for col in df.columns:
        # Cek beberapa baris pertama
        sample = df[col].dropna().head(10).astype(str)
        
        # Cek apakah ada pattern koordinat
        for val in sample:
            if re.search(r'[NS]\s*-?\d+\.?\d*\s+[EW]\s*-?\d+\.?\d*', val):
                coord_columns.append(col)
                break
    
    return coord_columns

def convert_excel_to_csv(excel_file, output_dir=None):
    """
    Konversi semua sheet Excel yang ada koordinat GPS menjadi CSV
    
    Parameters:
    -----------
    excel_file : str or Path
        Path ke file Excel
    output_dir : str or Path, optional
        Direktori output untuk file CSV. Default: sama dengan file Excel
    """
    excel_path = Path(excel_file)
    
    if output_dir is None:
        output_dir = excel_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
    
    # Baca semua sheet
    excel_data = pd.read_excel(excel_path, sheet_name=None)
    
    print(f"📊 Memproses file: {excel_path.name}")
    print(f"📄 Ditemukan {len(excel_data)} sheet\n")
    
    results = {}
    
    for sheet_name, df in excel_data.items():
        print(f"🔍 Memproses sheet: '{sheet_name}'")
        
        # Deteksi kolom koordinat
        coord_cols = detect_coordinate_columns(df)
        
        if not coord_cols:
            print(f"   ⚠️  Tidak ada kolom koordinat ditemukan\n")
            continue
        
        print(f"   ✓ Ditemukan {len(coord_cols)} kolom koordinat: {coord_cols}")
        
        # Buat copy dataframe
        df_converted = df.copy()
        
        # Konversi setiap kolom koordinat
        for col in coord_cols:
            print(f"   🔄 Mengkonversi kolom: {col}")
            
            # Parse koordinat
            coords = df[col].apply(parse_coord)
            
            # Buat kolom baru untuk latitude dan longitude
            lat_col = f"{col}_latitude"
            lon_col = f"{col}_longitude"
            
            df_converted[lat_col] = coords.apply(lambda x: x[0] if x else None)
            df_converted[lon_col] = coords.apply(lambda x: x[1] if x else None)
            
            # Hitung berapa yang berhasil dikonversi
            converted_count = df_converted[lat_col].notna().sum()
            total_count = df[col].notna().sum()
            
            print(f"      → Berhasil: {converted_count}/{total_count} koordinat")
        
        # Simpan ke CSV
        csv_filename = f"{excel_path.stem}_{sheet_name}.csv"
        csv_path = output_dir / csv_filename
        
        df_converted.to_csv(csv_path, index=False, encoding='utf-8-sig')
        
        results[sheet_name] = {
            'csv_path': csv_path,
            'rows': len(df_converted),
            'coord_columns': coord_cols
        }
        
        print(f"   ✅ Disimpan ke: {csv_path}\n")
    
    # Summary
    print("=" * 60)
    print("📋 RINGKASAN KONVERSI")
    print("=" * 60)
    
    for sheet_name, info in results.items():
        print(f"\nSheet: {sheet_name}")
        print(f"  File CSV: {info['csv_path'].name}")
        print(f"  Jumlah baris: {info['rows']}")
        print(f"  Kolom koordinat: {', '.join(info['coord_columns'])}")
    
    print(f"\n✨ Selesai! Total {len(results)} CSV file dibuat.")
    
    return results

# Contoh penggunaan
if __name__ == "__main__":
    # Ganti dengan path file Excel Anda
    excel_file = r"data/FORMAT_INPUT_DATA_INVENTARISASI_PJU_PERUMAHAN.xlsx"  # atau path lengkap
    
    # Konversi
    results = convert_excel_to_csv(excel_file)
    
    # Atau dengan output direktori khusus:
    # results = convert_excel_to_csv(excel_file, output_dir="output_csv")