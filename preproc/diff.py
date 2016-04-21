#import utils.imgs
import numpy as np
import cv2

def diff(in_path,out_path):
    img=cv2.imread(str(in_path))
    img=sign_diff(img)
    cv2.imwrite(str(out_path),img)

def sign_diff(img):
    img=basic_diff(img)
    print(img)
    img[img>0]=200.0
    img[img<0]=100.0
    return img

def full_diff(img):
    img=basic_diff(img)
    return np.abs(img)

def basic_diff(img):
    img_height=img.shape[0]/2
    img1=img[...][0:img_height]
    img2=img[...][img_height:2*img_height]
    img3=img2-img1
    return img3

if __name__ == "__main__":
    diff("out.jpg","diff.jpg")