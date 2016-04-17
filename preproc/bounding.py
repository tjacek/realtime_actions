import numpy as np
import cv2
#from utils.imgs import read_raw

def extract_box(img1,img2):
    p1,p2=moving_bbox(img1,img2)
    new_img1=img1[p1[0]:p2[0],p1[1]:p2[1]]
    return new_img1

def moving_bbox(img1,img2):
    points=[]
    points+=simple_bbox(img1)
    points+=simple_bbox(img2)
    points=np.array(points)
    print(points)
    x_dim=points[:,0]
    y_dim=points[:,1]
    return (min(y_dim),min(x_dim)),(max(y_dim),max(x_dim)) 

def simple_bbox(img):
    x0,y0,w,h=cv2.boundingRect(img)
    print((x0,y0))
    print((x0+w,y0+h))
    return [(x0,y0),((x0+w,y0+h))] 

def read_raw(img_path):
    return cv2.imread(str(img_path),cv2.IMREAD_GRAYSCALE) 

if __name__ == "__main__":
    img1=read_raw("in1.jpg")
    img2=read_raw("in2.jpg")
    new_img=extract_box(img1,img2)
    cv2.imwrite("out.jpg",new_img)