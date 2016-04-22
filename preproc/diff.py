#import utils.imgs
import numpy as np
import cv2
from utils.dirs import ApplyToDirs

NEG_VALUE=240
POZ_VALUE=200

@ApplyToDirs()
def diff(in_path,out_path):
    img=cv2.imread(str(in_path))
    img=smooth_diff(img)
    cv2.imwrite(str(out_path),img)

def smooth_diff(img):
    img = cv2.medianBlur(img,5)
    diff=basic_diff(img)
    print(diff<0)
    return diff

def sep_diff(img):
    img=standarize(img)
    diff_img=sign_diff(img)
    img1,img2=split_img(img)
    diff_img[diff_img!=0.0]=NEG_VALUE
    img1[img1==0]=diff_img[img1==0]
    return img1 

def coded_diff(img):
    img=standarize(img)
    diff_img=sign_diff(img)
    img1,img2=split_img(img)
    img1[diff_img==POZ_VALUE]+=64.0
    img1[diff_img==POZ_VALUE]+=127.0
    return img1

def standarize(img):
    max_value=np.max(img)
    img=img.astype(float)
    img/=max_value
    img*=128.0
    return img

def sign_diff(img):
    img=basic_diff(img)
    img[img>0]=POZ_VALUE
    img[img<0]=NEG_VALUE
    return img

def full_diff(img):
    img=basic_diff(img)
    return np.abs(img)

def basic_diff(img):
    img1,img2=split_img(img)
    img3=img2-img1
    return img3

def split_img(img):
    img_height=img.shape[0]/2
    img1=img[...][0:img_height]
    img2=img[...][img_height:2*img_height]	
    return img1,img2

if __name__ == "__main__":
    diff("out.jpg","diff.jpg")