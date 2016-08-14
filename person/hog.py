import sys,os
sys.path.append(os.path.abspath('../realtime_actions'))
import cv2
import utils.imgs
import utils.dirs
from skimage.feature import hog
import knn

class FindPerson(object):
    def __init__(self,in_path):
        pos_inst=self.get_features(in_path)[0]
        self.detector=knn.LazyCls(pos_inst)

    def __call__(self,in_path):
        feat,candidates=get_features(in_path)
        res=self.detector.best_match(feat)
        correct_img=candidates[res]
        return correct_img
        #print(correct_img.shape)

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

#find_person=FindPerson('person/train')

@utils.dirs.apply_to_dirs
def find(in_path,out_path):
    img_i=find_person(in_path)
    cv2.imwrite(str(out_path),img_i.get_orginal())

#find_person('person/in','out_path.jpg')
#find_person= utils.dirs.ApplyToFiles(find_person)
#find('../dataset6/segment','../dataset6/person')