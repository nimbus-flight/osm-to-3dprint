# osm-to-3dprint
Export OpenStreetMap (OSM) tiles, convert them to STL format, and import them directly into your 3D slicing software.

# Benefits
- free for commercial usage (MIT License)
- Larger Area Exports: Unlike Cadmapper, which limits free exports to 1 square kilometer, osm-to-3dprint allows you to export much larger areas without any cost.
- Optimized for 3D Printing: The exported STL files are designed to have no non-manifold edges, which ensures that the model is ready for 3D printing without the need for repairs.
- Small File Size: Despite covering extensive areas, the exported STL files are compact in size. For example, the entire downtown area of San Francisco (buildings.stl) is around ~17.5 MB (around 8.86 square kilometers).
- Relatively Fast - less than one minute to run main.py and get a city file for any given city.

# Features
- Customizable Parameters: Easily adjust parameters such as target size, maximum building height, and base thickness to suit your specific needs.
- Ready for Slicing: The generated STL files are optimized for 3D printing, ensuring minimal preparation time and reducing potential errors.

## Installation
```python3 -m pip install -r requirements.txt```

This project relies on several libraries, including OSM, overpass-api, osmnx, shapely, trimesh, and numpy-stl.

## Sample Usage
Adjust the GPS coordinates to define the bounding box of the area you wish to export:

```
# Example bounding box: min_lat, min_lon, max_lat, max_lon
bbox = (37.8049, 37.7749, -122.3894, -122.4194)  # San Francisco example
```

You can also modify parameters like target_size, max_height, and base_thickness to customize the export.

Run the script:
```python3 main.py```

# Future Improvements
- Additional Details: We're planning to include streets and other detailed features in future versions.
- Performance Enhancements: We aim to optimize the slicing software time, as it currently takes longer than expected for larger models.

## Example Output
Here's a sample of San Francisco visualized in Bambu Studio:
![image](https://github.com/user-attachments/assets/b2848b87-9a34-4516-8917-a705d83344de)


