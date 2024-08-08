import requests
import os

def fetch_osm_data(bbox):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:xml][timeout:25];
    (
      node["building"]({bbox});
      way["building"]({bbox});
      relation["building"]({bbox});
    );
    out body;
    >;
    out skel qt;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    response.encoding = 'utf-8'
    with open('map.osm', 'w', encoding='utf-8') as file:
        file.write(response.text)

# Example bounding box: min_lat, min_lon, max_lat, max_lon
bbox = "37.7749,-122.4194,37.8049,-122.3894"  # San Francisco example
fetch_osm_data(bbox)
