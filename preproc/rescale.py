import cv2
import numpy as np
#import utils.files as files

DIM_X=60
DIM_Y=60

def rescale(in_path,out_path):
    img=cv2.imread(in_path,cv2.IMREAD_GRAYSCALE)
    
    img=bounding_box(img)
    if(img==None):
        return None
    print(img.shape)
    res = cv2.resize(img,(DIM_X,DIM_Y), interpolation = cv2.INTER_CUBIC)
    proj=get_projections(res)
    cv2.imwrite(out_path,proj)

def bounding_box(img):
    ret,thresh = cv2.threshold(img,1,255,cv2.THRESH_BINARY)
    contours = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnt=contours[0]
    x_0,y_0,w,h=cv2.boundingRect(img)
    if(w==0 or h==0):
        return None
    x_w=x_0+w
    y_h=y_0+h
    return img[y_0:y_h,x_0:x_w]

def get_projections(img):
    height,width=img.shape
    z_max=np.amax(img)
    print(z_max)
    norm=float(width) / float(z_max+5)
    proj=np.zeros((height,3*width))
    for (x_i, y_i), element in np.ndenumerate(img):
        z_i=int(float(img[x_i][y_i]) * norm)
        if(z_i>10):      
            proj[x_i][y_i]=z_i
            proj[z_i][y_i+width]=100
            proj[x_i][z_i+2*width]=100
    return proj

if __name__ == "__main__":
    rescale("preproc/out.jpg","preproc/rescaled.jpg")