import cv2
import numpy as np
from skimage import measure

def get_single_component(in_path,out_path,watershed=False):
    img=cv2.imread(in_path,cv2.IMREAD_GRAYSCALE)
    if(watershed):
        img=water_component(img)
    else:
        img=ccomponents(img)
    cv2.imwrite(out_path,img)

def water_component(img):
    thresh=1
    ret,binary_img=cv2.threshold(img,1,255,cv2.THRESH_BINARY)
    #dist = cv2.distanceTransform(img,cv2.DIST_L2,5)
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(binary_img,cv2.MORPH_OPEN,kernel, iterations = 2)
    sure_bg = cv2.dilate(opening,kernel,iterations=3)
    dist = cv2.distanceTransform(opening,cv2.DIST_L2,5)
    ret, sure_fg = cv2.threshold(dist,0.2*dist.max(),255,0)
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)
    ret, markers = cv2.connectedComponents(sure_fg)
    markers = markers+1
    markers[unknown==255] = 0
    rgb_img=cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
    markers = cv2.watershed(rgb_img,markers)
    extract_max(img,markers)
    return img#markers*10

def extract_max(img,markers):
    n_comps=np.amax(markers)
    id_max_comp=max_component(markers,2)
    img[markers!=id_max_comp]=0

def ccomponents(img):
    ret,binary_img=cv2.threshold(img,1,255,cv2.THRESH_BINARY)
    seg_img = measure.label(binary_img,background=0)
    max_cc=max_component(seg_img)
    img[get_cc(max_cc,seg_img)]=0
    return seg_img    

def cc_size(i,comps):
    return comps[comps==i].shape[0]

def max_component(comps,lower=0):
    comp_sizes=[cc_size(i,comps) for i in range(lower,np.max(comps))]
    print(comp_sizes)
    comp_sizes=np.array(comp_sizes)
    return lower+comp_sizes.argmax(axis=0)

def get_cc(i,comps):
    return (comps!=i)

if __name__ == "__main__":
    get_single_component("in.jpg","out.jpg",True)