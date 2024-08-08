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

def get_building_height(row, default_height=10):
    # Check for various height attributes
    height_attrs = ['height', 'building:height', 'building:levels']
    for attr in height_attrs:
        if attr in row:
            height = row[attr]
            if isinstance(height, (int, float)) and not np.isnan(height):
                if attr == 'building:levels':
                    return height * 3  # Assuming 3 meters per level
                return height
            elif isinstance(height, str):
                try:
                    height_value = float(height.replace('m', '').strip())
                    return height_value
                except ValueError:
                    continue
    return default_height

def scale_coordinates(gdf, bbox, target_size=180, max_height_mm=40, default_height=10, base_thickness=4):
    # Calculate the scale factors for x and y dimensions
    north, south, east, west = bbox
    lat_range = north - south
    lon_range = east - west
    scale_x = target_size / lon_range
    scale_y = target_size / lat_range

    # Calculate maximum building height
    max_building_height = gdf.apply(lambda row: get_building_height(row, default_height), axis=1).max()
    height_scale = max_height_mm / max_building_height

    vertices = []
    faces = []

    # Base plane
    base_size = target_size * 1.2
    base_vertices = [
        (0, 0, -base_thickness),
        (base_size, 0, -base_thickness),
        (base_size, base_size, -base_thickness),
        (0, base_size, -base_thickness)
    ]
    
    base_faces = [
        [0, 1, 2],
        [0, 2, 3]
    ]

        # Create the base plane vertices and faces
    vertices = base_vertices.copy()
    faces = base_faces.copy()
    
    # Calculate center offsets
    center_x = base_size / 2
    center_y = base_size / 2
    
    # Add base vertices and faces
    vertices.extend(base_vertices)
    faces.extend(base_faces)

    for idx, row in gdf.iterrows():
        polygon = row['geometry']
        if isinstance(polygon, shapely.geometry.Polygon):
            exterior_coords = list(polygon.exterior.coords)
            base_index = len(vertices)

            # Determine height and scale it
            height = get_building_height(row, default_height) * height_scale
            print(f"Building at index {idx} with coordinates {exterior_coords} has height {height}")

            # Create vertices
            for coord in exterior_coords:
                v_bottom = ((coord[0] - west) * scale_x, (coord[1] - south) * scale_y, 0)
                v_top = ((coord[0] - west) * scale_x, (coord[1] - south) * scale_y, height)
                # Center buildings on the base
                v_bottom = (v_bottom[0] + (center_x - (target_size / 2)), v_bottom[1] + (center_y - (target_size / 2)), v_bottom[2])
                v_top = (v_top[0] + (center_x - (target_size / 2)), v_top[1] + (center_y - (target_size / 2)), v_top[2])
                
                vertices.extend([v_bottom, v_top])

            # Create side faces
            for i in range(len(exterior_coords) - 1):
                bottom1 = base_index + 2 * i
                bottom2 = base_index + 2 * (i + 1)
                top1 = base_index + 2 * i + 1
                top2 = base_index + 2 * (i + 1) + 1

                faces.append([bottom1, bottom2, top1])
                faces.append([top1, bottom2, top2])

            # Create top face
            top_face_indices = [base_index + 2 * i + 1 for i in range(len(exterior_coords) - 1)]
            for i in range(1, len(top_face_indices) - 1):
                faces.append([top_face_indices[0], top_face_indices[i], top_face_indices[i + 1]])

            # Create bottom face
            bottom_face_indices = [base_index + 2 * i for i in range(len(exterior_coords) - 1)]
            for i in range(1, len(bottom_face_indices) - 1):
                faces.append([bottom_face_indices[0], bottom_face_indices[i], bottom_face_indices[i + 1]])

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
    vertices, faces = scale_coordinates(gdf, bbox, target_size=180, max_height_mm=40, default_height=40, base_thickness=4)
    save_to_stl(vertices, faces, 'buildings.stl')

if __name__ == "__main__":
    main()
