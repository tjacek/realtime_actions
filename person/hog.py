import sys,os
sys.path.append(os.path.abspath('../realtime_actions'))
import cv2
import utils.imgs
from skimage.feature import hog
import knn

class FindPerson(object):
    def __init__(self,in_path):
        pos_inst=self.get_features(in_path)[0]
        self.detector=knn.LazyCls(pos_inst)

    def __call__(self,in_path,out_path):
        feat,candidates=self.get_features(in_path)
        res=self.detector.best_match(feat)
        correct_img=candidates[res]
        print(correct_img.shape)
        cv2.imwrite(out_path,correct_img.get_orginal())
        #print(res)
        #for feat_i in feat:
        #    print(feat_i.shape)
        #    print(feat_i[feat_i!=0])

    def get_features(self,in_path):
        candidates=utils.imgs.read_images(in_path)
        feat=[ self.compute(img_i)
                for img_i in candidates]
        return feat,candidates

    def compute(self,img_i):
    	img2D=img_i.get_orginal()
        fd = hog(img2D, orientations=8, pixels_per_cell=(24, 24),
                    cells_per_block=(1, 1), visualise=False)
        return fd

find_person=FindPerson('person/train')
find_person('person/in','out_path.jpg')