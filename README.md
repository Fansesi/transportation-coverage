# Public Transportation Coverage in Cities

Given a radius of walk distance, find the area that one may travel with only public transportation and walking. It may also be used for different building types (e.g. supermarkets) rather than transportations.

## Features
* Buffer Circles: Draw circles with a specified radius around latitude/longitude points.
* Union Areas: Calculate the total area covered by the circles, accounting for overlaps.
* Projection Handling: Use equal-area projections (e.g., EPSG:6933) to ensure accurate area measurements.
* Dynamic Mapping: Visualize circles and their union dynamically using folium.

## Requirements
* Python 3.7+
* geopandas
* shapely
* folium
* pyproj
* numpy

## Installation

Clone the repository and install the required Python libraries:

```bash
git clone https://github.com/fansesi/transportation-coverage.git
cd transportation-coverage
pip install -r requirements.txt
```

## Usage

### Data Collecting

For data collecting please refer to [data_collecting_via_overpass_api.md](data_collecting_via_overpass_api.md).

### Calculations

You may run the script via:

```bash
python calculate_coverage.py --geojson_path data/rayli_sistem_istasyon_poi_verisi.geojson --radius 200 --html_output_path saved_html_files/test_map.html
```

## License

This project is licensed under the MIT License.

## Acknowledgments
* [İBB Açık Veri Portalı](https://data.ibb.gov.tr/) for providing İstanbul's metro data. 
* [GeoPandas](https://geopandas.org/en/stable/) for spatial data manipulation.
* [Shapely](https://github.com/shapely/shapely) for geometric operations.
* [Folium](https://python-visualization.github.io/folium/latest/) for interactive mapping.
* [PyProj](https://github.com/pyproj4/pyproj) for CRS transformations.
