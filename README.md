# wowai-license-plate
## Installation
### Build from source
```
# Create and activate a virtual environment
conda create -n license_plate python=3.10 -y
source activate license_plate
 

# Install dependencies
pip install -r requirements.txt

# Install Darknet framework for YOLO
cd darknet && make
cd ..
  
# Download models: car-detector, lp-detector, and lp-ocr
bash get-networks.sh

# Create an empty directory for temporarily storing files
mkdir -p temp_dir

# Start the API
python app.py
```

### Docker
