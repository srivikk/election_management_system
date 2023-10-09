import xml.etree.ElementTree as ET
import os

# Specify the path to the directory containing LabelImg XML annotations
annotation_dir = 'data'  # Update the path to 'data'

# Specify the name of the XML file to convert
xml_file_name = 'coordinates.xml'

# Specify the output directory for Tesseract box files
output_dir = 'data/box_files'

os.makedirs(output_dir, exist_ok=True)

# Construct the full path to the XML file
xml_path = os.path.join(annotation_dir, xml_file_name)

# Check if the XML file exists
if os.path.isfile(xml_path):
    # Parse the XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Create a corresponding box file for the image
    image_filename = root.find('filename').text
    image_width = int(root.find('size/width').text)
    image_height = int(root.find('size/height').text)
    box_file_name = os.path.splitext(image_filename)[0] + '.box'
    box_file_path = os.path.join(output_dir, box_file_name)

    # Create and write to the box file
    with open(box_file_path, 'w') as box_file:
        for obj in root.findall('object'):
            label = obj.find('name').text
            bndbox = obj.find('bndbox')
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)

            # Calculate normalized coordinates
            norm_xmin = xmin / image_width
            norm_xmax = xmax / image_width
            norm_ymin = ymin / image_height
            norm_ymax = ymax / image_height

            # Write to the box file in Tesseract format
            box_file.write(f"{label} {norm_xmin:.6f} {norm_ymin:.6f} {norm_xmax:.6f} {norm_ymax:.6f}\n")
else:
    print(f"XML file '{xml_file_name}' not found in '{annotation_dir}'")

