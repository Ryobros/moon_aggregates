def parse_coord(line):
    a = line.split()

    # DDM
    if len(a) == 4:
        lat = (int(a[0][1:]) + float(a[1])/60) * (-1 if a[0][0]=="S" else 1)
        lon = (int(a[2][1:]) + float(a[3])/60) * (-1 if a[2][0]=="W" else 1)

    # DD
    elif len(a) == 2:
        lat = float(a[0][1:]) * (-1 if a[0][0]=="S" else 1)
        lon = float(a[1][1:]) * (-1 if a[1][0]=="W" else 1)

    else:
        raise ValueError(f"Format tidak dikenali: {line}")

    return lat, lon