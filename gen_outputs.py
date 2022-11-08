import sys

from license_plate_detection import OUTPUT_DIR
import cv2
import numpy as np

from glob						import glob
from os.path 					import splitext, basename, isfile
from src.utils 					import crop_region, image_files_from_folder
from src.drawing_utils			import draw_label, draw_losangle, write2img
from src.label 					import lread, Label, readShapes
from utils                   	import np_to_base64

from pdb import set_trace as pause

RED = (0,0,255)
GREEN = (0,255,0)


class OutputGenerator:
	def __init__(self):
		return
	
	def __call__(self, img_path, output_dir=OUTPUT_DIR):
		bname = splitext(basename(img_path))[0]
		img_org = cv2.imread(img_path)

		result = {
			"no_of_cars": 0,
			"cars": [],
			"image_output": None
		}

		detected_cars_labels = '%s/%s_cars.txt' % (output_dir,bname)
		label_cars = lread(detected_cars_labels)
		if label_cars:
			result['no_of_cars'] = len(label_cars)

			for idx, label_car in enumerate(label_cars):
				car = label_car.to_dict()
				car['top_left'] = car['top_left']*np.array(img_org.shape[1::-1], dtype=float).astype(int)
				car['top_left'] = car['top_left'].tolist()
				car['bot_right'] = car['bot_right']*np.array(img_org.shape[1::-1], dtype=float).astype(int)
				car['bot_right'] = car['bot_right'].tolist()
				car['license_plate'] = []
				car['license_plate_text'] = ''

				draw_label(img_org, label_car, color=RED, thickness=2)

				lp_label = '%s/%s_%dcar_lp.txt'	% (output_dir,bname,idx)
				lp_label_str 	= '%s/%s_%dcar_lp_str.txt'	% (output_dir,bname,idx)
				if isfile(lp_label):
					Llp_shapes = readShapes(lp_label)
					pts = Llp_shapes[0].pts*label_car.wh().reshape(2,1) + label_car.tl().reshape(2,1)
					ptspx = pts*np.array(img_org.shape[1::-1],dtype=float).reshape(2,1)
					

					car['license_plate'] = np.dstack(ptspx.astype(int))[0].reshape(1,-1)[0].tolist()

					draw_losangle(img_org,ptspx,GREEN,thickness=2)

					if isfile(lp_label_str):
						with open(lp_label_str,'r') as f:
							lp_str = f.read().strip()
						llp = Label(0,tl=pts.min(1),br=pts.max(1))
						write2img(img_org,llp,lp_str)

						car['license_plate_text'] = lp_str

				result['cars'].append(car)
		img_org = cv2.cvtColor(img_org, cv2.COLOR_BGR2RGB)
		img_base64 = np_to_base64(img_np=img_org)
		result['image_output'] = img_base64

		return result

# input_dir = sys.argv[1]
# output_dir = sys.argv[2]

# img_files = image_files_from_folder(input_dir)

# for img_file in img_files:

# 	result = {
# 			"no_of_cars": 0,
# 			"cars": [],
# 			"image_output": None
# 		}

# 	bname = splitext(basename(img_file))[0]

# 	I = cv2.imread(img_file)

# 	detected_cars_labels = '%s/%s_cars.txt' % (output_dir,bname)

# 	Lcar = lread(detected_cars_labels)

# 	sys.stdout.write('%s' % bname)

# 	if Lcar:
# 		result['no_of_cars'] = len(Lcar)

# 		for i,lcar in enumerate(Lcar):
# 			car = lcar.to_dict()
# 			car['top_left'] = car['top_left']*np.array(I.shape[1::-1], dtype=float).astype(int)
# 			car['bot_right'] = car['bot_right']*np.array(I.shape[1::-1], dtype=float).astype(int)
# 			car['lp'] = []
# 			car['lp_text'] = ''

# 			draw_label(I,lcar,color=YELLOW,thickness=3)

# 			lp_label 		= '%s/%s_%dcar_lp.txt'		% (output_dir,bname,i)
# 			lp_label_str 	= '%s/%s_%dcar_lp_str.txt'	% (output_dir,bname,i)

# 			if isfile(lp_label):

# 				Llp_shapes = readShapes(lp_label)
# 				pts = Llp_shapes[0].pts*lcar.wh().reshape(2,1) + lcar.tl().reshape(2,1)
# 				ptspx = pts*np.array(I.shape[1::-1],dtype=float).reshape(2,1)

# 				car['lp'] = np.dstack(ptspx.astype(int))[0].reshape(1,-1)[0].tolist()

# 				draw_losangle(I,ptspx,RED,3)

# 				if isfile(lp_label_str):
# 					with open(lp_label_str,'r') as f:
# 						lp_str = f.read().strip()
# 					llp = Label(0,tl=pts.min(1),br=pts.max(1))
# 					write2img(I,llp,lp_str)

# 					sys.stdout.write(',%s' % lp_str)

# 					car['lp_text'] = lp_str

# 			result['cars'].append(car)

# 	cv2.imwrite('%s/%s_output.png' % (output_dir,bname),I)
# 	print(result)
# 	sys.stdout.write('\n')


