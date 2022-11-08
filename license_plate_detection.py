import sys, os
import keras
import cv2
import traceback

from src.keras_utils 			import load_model
from glob 						import glob
from os.path 					import splitext, basename
from src.utils 					import im2single
from src.keras_utils 			import load_model, detect_lp
from src.label 					import Shape, writeShapes
from vehicle_detection 			import OUTPUT_DIR


WPOD_NET_PATH = 'data/lp-detector/wpod-net_update1.h5'


def adjust_pts(pts,lroi):
	return pts*lroi.wh().reshape((2,1)) + lroi.tl().reshape((2,1))

class LicensePlateDetector:
	def __init__(self, lp_model_path=WPOD_NET_PATH, threshold=0.5):
		self.lp_net = load_model(lp_model_path)
		self.threshold = threshold

	def __call__(self, input_dir=OUTPUT_DIR, output_dir=OUTPUT_DIR):
		imgs_path = glob('%s/*car.png' % input_dir)

		for idx, img_path in enumerate(imgs_path):
			bname = splitext(basename(img_path))[0]
			img_vehicle = cv2.imread(img_path)

			ratio = float(max(img_vehicle.shape[:2]))/min(img_vehicle.shape[:2])
			side  = int(ratio*288.)
			bound_dim = min(side + (side%(2**4)),608)

			list_lp,list_lp_imgs,_ = detect_lp(self.lp_net,im2single(img_vehicle),bound_dim,2**4,(240,80),self.threshold)
			if len(list_lp_imgs):
				img_lp = list_lp_imgs[0]
				img_lp = cv2.cvtColor(img_lp, cv2.COLOR_BGR2GRAY)
				img_lp = cv2.cvtColor(img_lp, cv2.COLOR_GRAY2BGR)

				s = Shape(list_lp[0].pts)
				cv2.imwrite('%s/%s_lp.png' % (output_dir,bname),img_lp*255.)
				writeShapes('%s/%s_lp.txt' % (output_dir,bname),[s])


# if __name__ == '__main__':
# 	try:
		
# 		input_dir  = sys.argv[1]
# 		output_dir = input_dir

# 		lp_threshold = .5

# 		wpod_net_path = sys.argv[2]
# 		wpod_net = load_model(wpod_net_path)

# 		imgs_paths = glob('%s/*car.png' % input_dir)

# 		print('Searching for license plates using WPOD-NET')

# 		for i,img_path in enumerate(imgs_paths):

# 			print('\t Processing %s' % img_path)

# 			bname = splitext(basename(img_path))[0]
# 			Ivehicle = cv2.imread(img_path)

# 			ratio = float(max(Ivehicle.shape[:2]))/min(Ivehicle.shape[:2])
# 			side  = int(ratio*288.)
# 			bound_dim = min(side + (side%(2**4)),608)
# 			print("\t\tBound dim: %d, ratio: %f" % (bound_dim,ratio))

# 			Llp,LlpImgs,_ = detect_lp(wpod_net,im2single(Ivehicle),bound_dim,2**4,(240,80),lp_threshold)


# 			if len(LlpImgs):
# 				print('======')
# 				print(Llp[0].pts)

# 				Ilp = LlpImgs[0]
# 				Ilp = cv2.cvtColor(Ilp, cv2.COLOR_BGR2GRAY)
# 				Ilp = cv2.cvtColor(Ilp, cv2.COLOR_GRAY2BGR)

# 				s = Shape(Llp[0].pts)
# 				cv2.imwrite('%s/%s_lp.png' % (output_dir,bname),Ilp*255.)
# 				writeShapes('%s/%s_lp.txt' % (output_dir,bname),[s])

# 	except:
# 		traceback.print_exc()
# 		sys.exit(1)

# 	sys.exit(0)


