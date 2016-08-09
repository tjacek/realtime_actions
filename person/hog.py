import sys,os
sys.path.append(os.path.abspath('../realtime_actions'))
#import cv2
import utils.imgs
from skimage.feature import hog

class FindPerson(object):

    def __call__(self,in_path):
        candidates=utils.imgs.read_images(in_path)
        feat=[ self.compute(img_i)
                for img_i in candidates]
        for feat_i in feat:
            print(feat_i.shape)
            print(feat_i[feat_i!=0])

    def compute(self,img_i):
    	img2D=img_i.get_orginal()
        fd = hog(img2D, orientations=8, pixels_per_cell=(24, 24),
                    cells_per_block=(1, 1), visualise=False)
        return fd

find_person=FindPerson()
find_person('person/in')