import os
import json
import sys
from shapely.ops import unary_union
from shapely.geometry import Polygon
from collections import Counter

def convert_bbox_to_yolo(bbox, img_width, img_height):
    """Convert bbox from [x_min, y_min, width, height] to YOLO format [x_center, y_center, width, height]."""
    x_min, y_min, w, h = bbox
    cx = (x_min + w / 2) / img_width
    cy = (y_min + h / 2) / img_height
    w /= img_width
    h /= img_height
    return cx, cy, w, h

def convert_segmentation_to_bbox(segmentation, img_width, img_height):
    """Convert segmentation polygon points to a bounding box."""
    if not segmentation or not isinstance(segmentation, list):
        return None  # Return None if segmentation data is invalid or not a list

    polygons = []
    for seg in segmentation:
        if isinstance(seg, list) and len(seg) >= 6:  # Ensure seg is a list and has at least 3 points (x, y pairs)
            try:
                polygon = Polygon([(seg[i], seg[i + 1]) for i in range(0, len(seg), 2)])
                polygons.append(polygon)
            except Exception as e:
                print(f"Error constructing polygon from points: {e}")
                continue  # Skip invalid polygon data

    if not polygons:
        return None  # No valid polygons formed

    # Merge all polygons into one and get the bounding box of the merged polygon
    merged_polygon = unary_union(polygons).envelope if polygons else None
    if not merged_polygon:
        return None  # No valid merged polygon

    x_min, y_min, x_max, y_max = merged_polygon.bounds
    return [x_min, y_min, x_max - x_min, y_max - y_min]  # bbox format [x_min, y_min, width, height]

def process_json_file(json_path, output_dir, class_counter, category_mapping):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    images = {img['id']: img for img in data['images']}
    
    file_initialized = set()  # Track initialized files to avoid multiple overwrites

    for annotation in data['annotations']:
        image_id = annotation['image_id']
        category_id = annotation['category_id']
        image_info = images.get(image_id)

        if not image_info:
            continue  # Skip if image not found

        img_width = image_info['width']
        img_height = image_info['height']
        file_name = image_info['file_name']
        txt_file_name = os.path.splitext(file_name)[0] + ".txt"
        txt_file_path = os.path.join(output_dir, txt_file_name)

        # Initialize file only once
        if txt_file_name not in file_initialized:
            with open(txt_file_path, 'w') as txt_file:  # Clear file content initially
                txt_file.write("")  # Empty content to initialize file
            file_initialized.add(txt_file_name)

        # Get bounding box, or calculate it from segmentation if bbox is empty
        bbox = annotation['bbox'] if annotation['bbox'] else convert_segmentation_to_bbox(annotation['segmentation'], img_width, img_height)
        if not bbox:
            continue  # Skip if no valid bbox or segmentation

        # Convert bbox to YOLO format
        cx, cy, w, h = convert_bbox_to_yolo(bbox, img_width, img_height)
        
        # Prepare YOLO annotation line
        class_id = category_id  # Assuming class_id starts from 0 for YOLO format
        class_counter[category_id] += 1  # Increment count for this class ID
        yolo_annotation = f"{class_id} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}\n"
        
        # Append to corresponding txt file
        with open(txt_file_path, 'a') as txt_file:  # Use 'a' to append objects
            txt_file.write(yolo_annotation)

def count_box(class_counter, category_mapping):
    """Print the count of objects per class with their string names, sorted by class ID."""
    print("="*50)
    for class_id, count in sorted(class_counter.items()):  # Sort by class_id
        class_name = category_mapping.get(class_id, "Unknown")
        print(f"Class {class_id} ({class_name}): {count}")
    
def parse_directory(root_dir):
    class_counter = Counter()  # Initialize a counter to track object counts per class
    category_mapping = {}  # To map category IDs to their names

    # Parse categories from the first JSON file
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.json'):
                json_path = os.path.join(subdir, file)
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    category_mapping = {cat['id']: cat['name'] for cat in data['categories']}
                break  # Parse categories once and break

    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.json'):
                json_path = os.path.join(subdir, file)
                # print(f"Processing {json_path}")
                process_json_file(json_path, subdir, class_counter, category_mapping)
    count_box(class_counter, category_mapping)  # Display class counts at the end

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python json_parse.py root")
        sys.exit(1)

    root_dir = sys.argv[1]
    parse_directory(root_dir)
