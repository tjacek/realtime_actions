import cv2
import numpy as np
from skimage import measure

def get_single_component(in_path,out_path):
    img=cv2.imread(in_path,cv2.IMREAD_GRAYSCALE)
    ret,binary_img=cv2.threshold(img,1,255,cv2.THRESH_BINARY)
    L = measure.label(binary_img,background=0)
    max_cc=max_component(L)
    img[get_cc(max_cc,L)]=0
    cv2.imwrite(out_path,img)

def cc_size(i,comps):
    return comps[comps==i].shape[0]

def max_component(comps):
    comp_sizes=[cc_size(i,comps) for i in range(np.max(comps))]
    print(comp_sizes)
    comp_sizes=np.array(comp_sizes)
    return comp_sizes.argmax(axis=0)

def get_cc(i,comps):
    return (comps!=i)

if __name__ == "__main__":
    get_single_component("in.jpg","out.jpg")