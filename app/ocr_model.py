import pytesseract
from PIL import Image
import cv2
import numpy as np

# Set the path to the Tesseract executable (replace with your actual path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

from pathlib import Path  # Add this import for handling paths

class OCRModel:
    def __init__(self, language='eng', tessdata_dir=None):
        """
        Initialize the OCR model.

        Args:
            language (str): The language code for Tesseract OCR (default is 'eng' for English).
            tessdata_dir (str): The path to the Tesseract language data directory.
        """
        self.language = language
        self.tessdata_dir = tessdata_dir

    def extract_text_from_image(self, image_path, all_coordinates):
        try:
            # Load the image using PIL
            img = Image.open(image_path)

            extracted_data = []  # Store extracted data for each set of coordinates

            # Iterate through all sets of coordinates
            for obj_name, coordinates in zip(["name", "middle_name", "house_number", "age", "gender"], all_coordinates):
                xmin, ymin, xmax, ymax = coordinates

                # Crop the image based on the provided coordinates
                cropped_img = img.crop((xmin, ymin, xmax, ymax))

                 # Convert the cropped image to grayscale
                gray_img = cv2.cvtColor(np.array(cropped_img), cv2.COLOR_RGB2GRAY)

                # Apply thresholding
                _, binary_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                # Use Tesseract OCR to extract text from the cropped region
                tessdata_dir_config = f'--tessdata-dir "{self.tessdata_dir}"' if self.tessdata_dir else ""
                psm_config = '--psm 6 --oem 1'  # Set the page segmentation mode
                text = pytesseract.image_to_string(binary_img, lang=self.language, config=f"{tessdata_dir_config} {psm_config}")

                # Create a dictionary for the extracted data
                extracted_dict = {
                    obj_name: text.strip()
                }

                # Append the dictionary to the list
                extracted_data.append(extracted_dict)

            return extracted_data
        except Exception as e:
            return str(e)
