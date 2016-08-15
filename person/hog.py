import sys,os
sys.path.append(os.path.abspath('../realtime_actions'))
import cv2
import utils.imgs
import utils.dirs
from skimage.feature import hog
import knn
import deep
import numpy as np

class FindPerson(object):
    def __init__(self,detector):
        self.detector=detector

    def __call__(self,in_path,out_path):
        feat,candidates=get_features(in_path)
        res=self.best_match(feat)
        print(res)
        correct_img=candidates[res]
        cv2.imwrite(str(out_path),correct_img.get_orginal())
        return correct_img
        #print(correct_img.shape)

    def best_match(self,candidates):
        dist=[ self.detector(cand_i)
               for cand_i in candidates]
        return np.argmin(dist)

def get_features(in_path):
    candidates=utils.imgs.read_images(in_path)
    feat=[ compute(img_i)
                for img_i in candidates]
    return feat,candidates

def compute(img_i):
    img2D=img_i.get_orginal()
    fd = hog(img2D, orientations=8, pixels_per_cell=(24, 24),
                    cells_per_block=(1, 1), visualise=False)
    return fd

if __name__ == "__main__":
    deep_cls=deep.load_cls()
    find_person=FindPerson(deep_cls)
    @utils.dirs.apply_to_dirs
    def find(in_path,out_path):
        img_i=find_person(in_path,out_path)
    find('../dataset6/segment','../dataset6/person')
#find_person('person/in','out_path.jpg')
#find_person= utils.dirs.ApplyToFiles(find_person)
#find('../dataset6/segment','../dataset6/person')