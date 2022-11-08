# wowai-license-plate
## Installation
### a. Build from source
```
# Create and activate a virtual environment
$ conda create -n license_plate python=3.10 -y
$ source activate license_plate
 

# Install dependencies
$ pip install -r requirements.txt

# Install Darknet framework for YOLO
$ cd darknet && make
$ cd ..
  
# Download models: car-detector, lp-detector, and lp-ocr
$ bash get-networks.sh

# Create an empty directory for temporarily storing files
$ mkdir -p temp_dir

# Start the API
$ python app.py
```

### b. Install via Docker
```
$ sudo docker build -t wowai/license-plate .
$ sudo docker run --name license-plate -p 5000:5000 wowai/license-plate
```
The API is then available at http://0.0.0.0:5000/

## API Endpoints
### 1. POST /license-plate
Detect and extract license plates from images
#### Request body
Key | Description | Type | Note
|--------|----------|--------|--------|
images| Input images, which contains cars with license plates| multipart/form-data| required|

#### Response
Successful response will return a json with following fields:
Key | Description | Type |
|--------|----------|--------|
no_of_cars| Number of cars detected| int|
cars| List of cars detected and their information| list| 
car.top_left| [x,y]- coordinate of the top left of bounding box | [float, float]|
car.bot_right| [x,y] - coordinate of the bottom right of bounding box | [float, float]|
car.license_plate | [x,y,x,y,...] - the 4 points of detected license plates| [int]|
car.license_plate_text | The text extracted from license plates | string| 
