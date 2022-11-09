# wowai-license-plate
## 1. INSTALLATION
There are two methods to install and run the api: from source or via Docker
### a. Build from source
```
# Create and activate a virtual environment
$ conda create -n license_plate python=3.10 -y
$ conda activate license_plate
 

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
$ docker build -t wowai/license-plate .
$ docker run --name license-plate -p 5000:5000 wowai/license-plate
```
The API is then available at http://0.0.0.0:5000/

**Note:** the original repository is developed and run on Ubuntu 22.04 LTS and haven't been tested on any other OS yet.

## 2. API ENDPOINTS
### 2.1 POST /license_plate
Detect and extract license plates from image <br/>
Request URL: http://0.0.0.0:5000/license_plate <br/>
#### Request body
Key | Description | Type | Note
|--------|----------|--------|--------|
image| Input image, which contains cars with license plates| multipart/form-data| required|

#### Response
Successful response (Code 200) will return a json with following fields:
Key | Description | Type |
|--------|----------|--------|
no_of_cars| Number of cars detected| int|
cars| List of cars detected and their information| list| 
car.top_left| [x,y] - coordinate of the top left of bounding box | [float, float]|
car.bot_right| [x,y] - coordinate of the bottom right of bounding box | [float, float]|
car.prob| Probability of prediction, can be null| float|
car.license_plate | [x,y,x,y,...] - the 4 points of detected license plates| [int]|
car.license_plate_text | The text extracted from license plates | string|
image_output| Output image with extracted information| base64 string|

## 3. DEMO
Here is an example of successful response:
```
{
    "message": "successful",
    "results": {
        "no_of_cars": 1,
        "cars": [
            {
                "class": "car",
                "top_left": [
                    498.5275260000001,
                    731.8284255
                ],
                "bot_right": [
                    1398.737178,
                    1249.8060645
                ],
                "prob": null,
                "license_plate": [
                    794,
                    1068,
                    1037,
                    1066,
                    1037,
                    1123,
                    794,
                    1125
                ],
                "license_plate_text": "MPC7772"
            }
        ],
        "image_output": "data:image/png;base64,iVBOR..."
    }
}
```
Note that *image_output* is a base64 string encode for the final image as below:

![licenseplate1_output](https://user-images.githubusercontent.com/79528257/200648494-271f1d53-7181-43f3-a6ea-1a6796870163.png)
