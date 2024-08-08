# osm-to-3dprint
Export Open Street Map tiles, convert to OBJ for importing to 3D slicing software

## install requirements
```python3 -m pip install -r requirements.txt```

This library depends on osm, overpass-api, osmnx

## sample usage
change gps coordinates for bounding box

```
# Example bounding box: min_lat, min_lon, max_lat, max_lon
bbox = "37.7749,-122.4194,37.8049,-122.3894"  # San Francisco example
```

## change target_size, max_height, and base thickness parameters
```python3 main.py```


## sample of San Francisco in Bambu Studio
![image](https://github.com/user-attachments/assets/47d082ec-26f0-4698-87a6-0d0c1606c6bf)


