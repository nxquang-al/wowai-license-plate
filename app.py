import os
import glob
import uvicorn

from fastapi                 import FastAPI, UploadFile, File
from vehicle_detection       import VehicleDetector
from license_plate_detection import LicensePlateDetector
from license_plate_ocr       import LicensePlateOCR
from gen_outputs             import OutputGenerator

app = FastAPI()
TEMP_DIR = "./temp_dir"

vehicle_detector = VehicleDetector()
lp_detector = LicensePlateDetector()
lp_ocr = LicensePlateOCR()
output_generator = OutputGenerator()

@app.get('/')
def index():
    return{
        "message": "hello world"
    }

@app.post("/license_plate")
async def lp_extract(image: UploadFile=File(...)):
    try:
        content = image.file.read()
        img_path = os.path.join(TEMP_DIR, image.filename)
        with open(img_path, 'wb') as f:
            f.write(content)
        
        list_cars = vehicle_detector(img_path=img_path)
        lp_detector(input_dir=TEMP_DIR, output_dir=TEMP_DIR)
        lp_ocr(input_dir=TEMP_DIR, output_dir=TEMP_DIR)
        output = output_generator(img_path=img_path, output_dir=TEMP_DIR)
        
    except Exception:
        return{
            "message": "fail",
            "results": {}
        }
    finally:
        image.file.close()
        for f in glob.glob(TEMP_DIR + '/*'):
            os.remove(f)
    return{
            "message": "successful",
            "results": output 
        }

if __name__== "__main__":
    port = int(os.environ.get('PORT', 5000))
    uvicorn.run("app:app", host='0.0.0.0', port=port, reload=True)