import folium.features
import numpy as np
from shapely.geometry import Point
from shapely.ops import unary_union
import pyproj
import folium
import folium.plugins
from folium import GeoJson
from shapely.geometry import Point
from shapely.ops import unary_union
import webbrowser
import pandas as pd
import geopandas as gpd
import argparse
from pathlib import Path


def calculate_union_and_area(lat_lon, radius):
    # Project lat/lon to a planar CRS for accurate area calculations
    transformer = pyproj.Transformer.from_crs(
        "EPSG:4326", "EPSG:3857", always_xy=True
    )  # WGS84 to Web Mercator

    circles = []
    for lat, lon in lat_lon:
        x, y = transformer.transform(lon, lat)
        circles.append(
            Point(x, y).buffer(radius)
        )  # Create circles in projected coordinates

    # Calculate union of circles
    union = unary_union(circles)
    total_area = union.area  # Area in m^2
    return union, total_area


def import_csv_data(csv_path: str):
    """Returns dataframe and only lat and lon values in a np.array."""
    df = pd.read_table(csv_path)
    lat_lon = np.stack((df["lat"], df["lon"]), axis=1)
    return df, lat_lon


def import_geojson_data(geojson_path: str):
    gdf = gpd.read_file(geojson_path)
    lat_lon = np.array([(geom.y, geom.x) for geom in gdf.geometry])

    return gdf, lat_lon


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Calculate areas of circles and generate an interactive map."
    )

    # Add arguments
    parser.add_argument(
        "--geojson_path",
        type=str,
        help="Path to the input data file containing latitude and longitude.",
        # default="data/rayli_sistem_istasyon_poi_verisi.geojson",
        required=False,
    )
    parser.add_argument(
        "--csv_path",
        type=str,
        help="Path to the input data file containing latitude and longitude.",
        # default="data/overpass - bus stops.csv",
        required=False,
    )
    parser.add_argument(
        "--radius", type=int, help="Radius of the circles in meters.", default=1000
    )
    parser.add_argument(
        "--html_output_path",
        type=str,
        help="Path to save the generated HTML map.",
        default="savedhtml_files/map.html",
    )

    args = parser.parse_args()

    if args.csv_path == None and args.geojson_path == None:
        raise KeyError("You should specify one of these: csv_path or geojson_path.")

    # Parse arguments
    return args


if __name__ == "__main__":
    args = parse_arguments()
    if args.csv_path != None:
        df, lat_lon = import_csv_data(args.csv_path)
    else:
        df, lat_lon = import_geojson_data(args.geojson_path)

    ### Without argparse
    # For bus stops
    # df, lat_lon = import_csv_data("data/overpass - bus stops.csv")

    # For metros
    # df, lat_lon = import_geojson_data(
    #     "data/ibb/rayli_sistem_istasyon_poi_verisi.geojson"
    # )

    radius = args.radius
    # radius = 500  # in meters

    # Get the union geometry and total area
    union_geom, total_area = calculate_union_and_area(lat_lon, radius)

    # Convert the union geometry to GeoJSON for Folium
    project_back = pyproj.Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)

    # Handle MultiPolygon or Polygon for union geometry
    features = []
    if union_geom.geom_type == "Polygon":
        exterior_coords = [
            project_back.transform(x, y) for x, y in union_geom.exterior.coords
        ]
        features.append(
            {
                "type": "Feature",
                "geometry": {"type": "Polygon", "coordinates": [exterior_coords]},
            }
        )
    elif union_geom.geom_type == "MultiPolygon":
        for polygon in union_geom.geoms:
            exterior_coords = [
                project_back.transform(x, y) for x, y in polygon.exterior.coords
            ]
            features.append(
                {
                    "type": "Feature",
                    "geometry": {"type": "Polygon", "coordinates": [exterior_coords]},
                }
            )

    geojson = {"type": "FeatureCollection", "features": features}

    # Create a Folium map centered on the average location
    # center_lat = sum(lat for lat, lon in lat_lon) / len(lat_lon)
    # center_lon = sum(lon for lat, lon in lat_lon) / len(lat_lon)lat_lon.mean(axis=1)[0]
    m = folium.Map(
        location=[lat_lon.mean(axis=1)[0], lat_lon.mean(axis=1)[1]], zoom_start=3
    )

    # Add the points and circles
    for lat, lon in lat_lon:
        folium.Marker(location=[lat, lon], popup=f"Point: {lat}, {lon}").add_to(m)
        folium.Circle(
            location=[lat, lon],
            radius=radius,
            color="blue",
            fill=True,
            fill_opacity=0.4,
        ).add_to(m)

    # Add the result
    folium.Marker(
        [40.93, 28.89],
        icon=folium.features.DivIcon(
            icon_size=(400, 1200),
            icon_anchor=(0, 0),
            html=f'<div style="font-size: 15pt">Total area of the circles (accounting for overlap): {total_area / 1e6:.2f} km²</div>',
        ),
    ).add_to(m)

    # Add the union geometry as a GeoJSON overlay
    GeoJson(data=geojson, name="Union of Circles").add_to(m)

    # Add a legend
    folium.LayerControl().add_to(m)

    # Save the map to an HTML file and open it
    # save_location = f"saved_html_files/istanbul_busses - with {radius} radius.html"
    _save_path = Path(args.html_output_path)
    save_location = (
        str(_save_path.parent)
        + "/"
        + _save_path.stem
        + f" with {radius} meter radius.html"
    )

    m.save(save_location)
    webbrowser.open(save_location, new=2)

    # Display the total area
    print(
        f"Total area of the circles (accounting for overlap): {total_area / 1e6:.2f} km²"
    )
