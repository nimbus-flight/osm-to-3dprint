import osmnx as ox
import shapely
import numpy as np
from stl import mesh

def fetch_building_data(bbox):
    # Define the bounding box (north, south, east, west)
    north, south, east, west = bbox
    # Fetch building footprints within the bounding box
    gdf = ox.geometries_from_bbox(north, south, east, west, tags={'building': True})
    return gdf

def scale_coordinates(gdf, bbox, target_size=200, default_height=10):
    # Calculate the scale factors for x and y dimensions
    north, south, east, west = bbox
    lat_range = north - south
    lon_range = east - west
    scale_x = target_size / lon_range
    scale_y = target_size / lat_range

    vertices = []
    faces = []
    for polygon in gdf['geometry']:
        if isinstance(polygon, shapely.geometry.Polygon):
            exterior_coords = polygon.exterior.coords
            base_index = len(vertices)
            for i in range(len(exterior_coords) - 1):
                v0 = exterior_coords[i]
                v1 = exterior_coords[(i + 1) % len(exterior_coords)]
                # Scale the coordinates
                v0_3d = ((v0[0] - west) * scale_x, (v0[1] - south) * scale_y, 0)
                v1_3d = ((v1[0] - west) * scale_x, (v1[1] - south) * scale_y, 0)
                height = default_height if 'building:levels' not in gdf else gdf['building:levels'].get(polygon, default_height) * 3  # Assuming 3 meters per level
                v0_3d_top = (v0_3d[0], v0_3d[1], height)
                v1_3d_top = (v1_3d[0], v1_3d[1], height)
                vertices.extend([v0_3d, v1_3d, v0_3d_top, v1_3d_top])

                # Side faces
                faces.append([base_index, base_index + 1, base_index + 2])
                faces.append([base_index + 2, base_index + 1, base_index + 3])

                base_index += 4
    vertices = np.array(vertices)
    faces = np.array(faces)
    return vertices, faces

def save_to_stl(vertices, faces, filename):
    mesh_data = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, face in enumerate(faces):
        for j in range(3):
            mesh_data.vectors[i][j] = vertices[face[j], :]
    mesh_data.save(filename)

def main():
    # Example bounding box: (north, south, east, west)
    bbox = (37.8049, 37.7749, -122.3894, -122.4194)  # San Francisco example
    gdf = fetch_building_data(bbox)
    vertices, faces = scale_coordinates(gdf, bbox, target_size=200, default_height=40)
    save_to_stl(vertices, faces, 'buildings.stl')

if __name__ == "__main__":
    main()
