from flask import Blueprint, request, Response, jsonify, render_template  # Import render_template
from .ocr_model import OCRModel
import os
from pdf2image import convert_from_bytes
import xml.etree.ElementTree as ET

ocr_bp = Blueprint("ocr", __name__)

# Specify the directory to save PDF images
PDF_IMAGES_DIR = "data/images"

# Path to the XML file containing coordinates
XML_FILE_PATH = "data/coordinates.xml"

@ocr_bp.route("/api/extract_text", methods=["POST"])
def extract_text():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        # Read the XML data from the file
        with open(XML_FILE_PATH, "r") as xml_file:
            xml_data = xml_file.read()

        # Parse the XML data
        xml_root = ET.fromstring(xml_data)

        # Get the language parameter from the request
        language = request.form.get("language", "eng")

        # Initialize the OCR model with the selected language
        ocr_model = OCRModel(language)

        # Initialize a dictionary to store extracted data for each object name
        extracted_data = {}

        # Check if the file is a PDF
        if file.filename.lower().endswith(".pdf"):
            # Create the directory to save PDF images
            os.makedirs(PDF_IMAGES_DIR, exist_ok=True)

            try:
                # Convert the PDF to images
                pdf_images = convert_from_bytes(file.read(), output_folder=PDF_IMAGES_DIR)
            except Exception as pdf_error:
                return jsonify({"error": f"Error processing PDF: {str(pdf_error)}"}), 400

            # Process each image and extract text
            for i, image in enumerate(pdf_images):
                image_path = os.path.join(PDF_IMAGES_DIR, f"page_{i + 1}.jpg")

                # Iterate through all objects in the XML
                for obj_elem in xml_root.findall("object"):
                    obj_name = obj_elem.find("name").text
                    coord_elem = obj_elem.find("bndbox")
                    if coord_elem is not None:
                        xmin = int(coord_elem.find("xmin").text)
                        ymin = int(coord_elem.find("ymin").text)
                        xmax = int(coord_elem.find("xmax").text)
                        ymax = int(coord_elem.find("ymax").text)

                        # Crop and extract text as before
                        data = ocr_model.extract_text_from_image(image_path, [(xmin, ymin, xmax, ymax)])[0]

                        # Append the extracted data to the respective object's list
                        if obj_name not in extracted_data:
                            extracted_data[obj_name] = []
                        extracted_data[obj_name].append(data)

                # Save the processed image
                image.save(image_path, "JPEG")

            # Clean up: remove temporary PDF images
            for image_path in os.listdir(PDF_IMAGES_DIR):
                os.remove(os.path.join(PDF_IMAGES_DIR, image_path))
            os.rmdir(PDF_IMAGES_DIR)

        # Handle other file formats (e.g., images) using Tesseract OCR
        else:
            # Save the image as a temporary file
            temp_image_path = os.path.join(PDF_IMAGES_DIR, "temp_image.jpg")
            file.save(temp_image_path)

            # Iterate through all objects in the XML
            for obj_elem in xml_root.findall("object"):
                obj_name = obj_elem.find("name").text
                coord_elem = obj_elem.find("bndbox")
                if coord_elem is not None:
                    xmin = int(coord_elem.find("xmin").text)
                    ymin = int(coord_elem.find("ymin").text)
                    xmax = int(coord_elem.find("xmax").text)
                    ymax = int(coord_elem.find("ymax").text)

                    # Crop and extract text as before
                    data = ocr_model.extract_text_from_image(temp_image_path, [(xmin, ymin, xmax, ymax)])[0]

                    # Append the extracted data to the respective object's list
                    if obj_name not in extracted_data:
                        extracted_data[obj_name] = []
                    extracted_data[obj_name].append(data)

            # Remove the temporary image file
            os.remove(temp_image_path)

        # Convert the extracted data dictionary to a list of dictionaries
        extracted_data_list = [{"name": obj_name, "data": data} for obj_name, data in extracted_data.items()]


        # Initialize an empty dictionary to store the output data
        output_data = {}

        # Iterate through input_data and extract values into the output_data dictionary
        for item in extracted_data_list:
            field_name = item["name"]
            field_values = [element["name"] for element in item["data"]]
            output_data[field_name] = field_values

        # Convert the output data dictionary to an array of objects for each element
        output_list = []

        # Determine the number of elements in each field (assuming all fields have the same number of elements)
        num_elements = len(output_data[list(output_data.keys())[0]])

        # Iterate through the elements and create objects
        for i in range(num_elements):
            output_obj = {}
            for field_name, field_values in output_data.items():
                output_obj[field_name] = field_values[i]
            output_list.append(output_obj)

        print(output_list)

        # Return the extracted data as a JSON response
        return jsonify(output_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle exceptions and return an appropriate error response

@ocr_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")
