# Create a virtual environment
python -m venv venv

# Activate the virtual environment (on Windows)
venv\Scripts\activate

# Activate the virtual environment (on macOS/Linux)
source venv/bin/activate

# Install dependencies
# a. Manually
pip install Flask tensorflow pillow PyMuPDF pdf2image

#b. To directly install dependencies from requirements.txt
pip install -r requirements.txt

# To run flask application
python app.py

# Install poppler to use pdf2image library