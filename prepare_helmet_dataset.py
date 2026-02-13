import os
import xml.etree.ElementTree as ET
import shutil
from pathlib import Path
import random

# Paths
source_images = r"C:\Users\svlak\Downloads\hel-met\images"
source_annotations = r"C:\Users\svlak\Downloads\hel-met\annotations"
output_base = r"C:\Users\svlak\New folder (14)\helmet_detection"

# Class mapping
class_names = ["With Helmet", "Without Helmet"]
class_to_idx = {name: idx for idx, name in enumerate(class_names)}

def convert_box_to_yolo(size, box):
    """Convert Pascal VOC box to YOLO format."""
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    
    x_center = (box[0] + box[2]) / 2.0
    y_center = (box[1] + box[3]) / 2.0
    width = box[2] - box[0]
    height = box[3] - box[1]
    
    x_center *= dw
    y_center *= dh
    width *= dw
    height *= dh
    
    return (x_center, y_center, width, height)

def parse_xml_annotation(xml_file):
    """Parse Pascal VOC XML annotation file."""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    size = root.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)
    
    annotations = []
    for obj in root.findall('object'):
        class_name = obj.find('name').text
        
        if class_name not in class_to_idx:
            print(f"Warning: Unknown class '{class_name}' in {xml_file}")
            continue
        
        class_idx = class_to_idx[class_name]
        
        bbox = obj.find('bndbox')
        xmin = float(bbox.find('xmin').text)
        ymin = float(bbox.find('ymin').text)
        xmax = float(bbox.find('xmax').text)
        ymax = float(bbox.find('ymax').text)
        
        yolo_box = convert_box_to_yolo((width, height), (xmin, ymin, xmax, ymax))
        annotations.append((class_idx, *yolo_box))
    
    return annotations

def create_dataset():
    """Create YOLO format dataset from Pascal VOC annotations."""
    print("Starting dataset preparation...")
    
    # Create directory structure
    for split in ['train', 'val']:
        for folder in ['images', 'labels']:
            path = Path(output_base) / split / folder
            path.mkdir(parents=True, exist_ok=True)
            print(f"Created: {path}")
    
    # Get all annotation files
    annotation_files = list(Path(source_annotations).glob("*.xml"))
    print(f"\nFound {len(annotation_files)} annotation files")
    
    # Shuffle and split
    random.seed(42)
    random.shuffle(annotation_files)
    
    train_split = int(0.8 * len(annotation_files))
    train_files = annotation_files[:train_split]
    val_files = annotation_files[train_split:]
    
    print(f"Train set: {len(train_files)} images")
    print(f"Val set: {len(val_files)} images\n")
    
    # Process each split
    for split_name, file_list in [('train', train_files), ('val', val_files)]:
        print(f"Processing {split_name} set...")
        
        for xml_file in file_list:
            # Get image filename
            image_name = xml_file.stem + ".png"
            image_path = Path(source_images) / image_name
            
            if not image_path.exists():
                print(f"Warning: Image not found: {image_path}")
                continue
            
            # Parse annotations
            try:
                annotations = parse_xml_annotation(xml_file)
            except Exception as e:
                print(f"Error parsing {xml_file}: {e}")
                continue
            
            # Copy image
            dest_image = Path(output_base) / split_name / 'images' / image_name
            shutil.copy2(image_path, dest_image)
            
            # Write YOLO format labels
            dest_label = Path(output_base) / split_name / 'labels' / (xml_file.stem + ".txt")
            with open(dest_label, 'w') as f:
                for ann in annotations:
                    f.write(f"{ann[0]} {ann[1]:.6f} {ann[2]:.6f} {ann[3]:.6f} {ann[4]:.6f}\n")
        
        print(f"Completed {split_name} set\n")
    
    print("Dataset preparation complete!")
    print(f"\nDataset location: {output_base}")
    print(f"Train images: {len(list((Path(output_base) / 'train' / 'images').glob('*.png')))}")
    print(f"Val images: {len(list((Path(output_base) / 'val' / 'images').glob('*.png')))}")

if __name__ == "__main__":
    create_dataset()
