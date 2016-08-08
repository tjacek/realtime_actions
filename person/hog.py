import sys,os
sys.path.append(os.path.abspath('../realtime_actions'))
import cv2
import utils.imgs

class FindPerson(object):
    def __init__(self):
        self.hog = cv2.HOGDescriptor()

    def __call__(self,in_path):
        candidates=utils.imgs.read_images(in_path)
        feat=[ self.hog.compute(img_i.get_orginal())
                for img_i in candidates]
        for feat_i in feat:
            print(feat_i.shape)
            print(feat_i[feat_i!=0])
#def clean(out_path):
#    grey_img = cv2.imread(grey_path)
#    rgb_img= cv2.imread(rgb_path)
#    rgb_img=cv2.resize(rgb_img, (0,0), fx=0.5, fy=0.5)
#    print(grey_img.shape)
#    print(rgb_img.shape)
#    rgb_img[grey_img==0]=0
#    cv2.imwrite(out_path,rgb_img)

find_person=FindPerson()
find_person('person/in')