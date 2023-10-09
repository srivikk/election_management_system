#Intallation and launch guide for labelImg -> GUI for image and pdf annotation

# Installation using pip:
pip install labelImg

# Installation from source:

# a. Clone the LabelImg repository from GitHub:
git clone https://github.com/tzutalin/labelImg.git

# b. Navigate to the LabelImg directory:
cd labelImg

# c. Install the required dependencies (Qt, PyQt5, lxml):
# On Ubuntu/Debian:

sudo apt-get install python3-pyqt5
sudo apt-get install pyqt5-dev-tools
sudo pip install -r requirements/requirements-linux-python3.txt

# On Windows, you'll need to manually install PyQt5 and lxml using pip:
pip install pyqt5 lxml

# d. Build the LabelImg resources:

pyrcc5 -o libs/resources.py resources.qrc

# e. Run LabelImg:
python labelImg.py
