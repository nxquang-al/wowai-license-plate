import enum
import sys

from vehicle_detection import OUTPUT_DIR
import cv2
import numpy as np
import traceback

import darknet.python.darknet as dn

from os.path 				import splitext, basename
from glob					import glob
from darknet.python.darknet import detect
from src.label				import dknet_label_conversion
from src.utils 				import nms
# from matplotlib				import pyplot as plt
# from PIL					import Image


WEIGHTS = bytes('data/ocr/ocr-net.weights', encoding='utf-8')
CONFIG = bytes('data/ocr/ocr-net.cfg', encoding="utf-8")
DATASET = bytes('data/ocr/ocr-net.data', encoding="utf-8")
OUTPUT_DIR = 'tmp/output'

class LicensePlateOCR:
	def __init__(self, weights=WEIGHTS, config=CONFIG, dataset=DATASET, threshold=0.4):
		self.ocr_net = dn.load_net(config, weights, 0)
		self.ocr_meta = dn.load_meta(dataset)
		self.threshold = threshold

	def __call__(self, input_dir=OUTPUT_DIR, output_dir=OUTPUT_DIR):
		imgs_paths = sorted(glob('%s/*lp.png' % input_dir))

		for idx, img_path in enumerate(imgs_paths):
			bname = basename(splitext(img_path)[0])
			img_path = bytes(img_path, encoding="utf-8")

			predictions,(width,height) = detect(self.ocr_net, self.ocr_meta, img_path ,thresh=self.threshold, nms=None)
			if len(predictions):
				L = dknet_label_conversion(predictions,width,height)
				L = nms(L,.45)

				L.sort(key=lambda x: x.tl()[0])
				lp_str = ''.join([chr(l.cl()) for l in L])

				with open('%s/%s_str.txt' % (output_dir,bname),'w') as f:
					f.write(lp_str + '\n')				
			


# if __name__ == '__main__':

# 	try:
	
# 		input_dir  = sys.argv[1]
# 		output_dir = input_dir

# 		ocr_threshold = .4

# 		ocr_weights = bytes('data/ocr/ocr-net.weights', encoding='utf-8')
# 		ocr_netcfg  = bytes('data/ocr/ocr-net.cfg', encoding="utf-8")
# 		ocr_dataset = bytes('data/ocr/ocr-net.data', encoding="utf-8")

# 		ocr_net  = dn.load_net(ocr_netcfg, ocr_weights, 0)
# 		ocr_meta = dn.load_meta(ocr_dataset)

# 		imgs_paths = sorted(glob('%s/*lp.png' % output_dir))

# 		print('Performing OCR...')

# 		for i,img_path in enumerate(imgs_paths):

# 			print('\tScanning %s' % img_path)

# 			bname = basename(splitext(img_path)[0])
			
# 			img_path = bytes(img_path, encoding="utf-8")

# 			R,(width,height) = detect(ocr_net, ocr_meta, img_path ,thresh=ocr_threshold, nms=None)

# 			if len(R):

# 				L = dknet_label_conversion(R,width,height)
# 				L = nms(L,.45)

# 				L.sort(key=lambda x: x.tl()[0])
# 				lp_str = ''.join([chr(l.cl()) for l in L])

# 				with open('%s/%s_str.txt' % (output_dir,bname),'w') as f:
# 					f.write(lp_str + '\n')

# 				print('\t\tLP: %s' % lp_str)

# 			else:

# 				print('No characters found')

# 	except:
# 		traceback.print_exc()
# 		sys.exit(1)

# 	sys.exit(0)
