#import utils.imgs
import numpy as np
import cv2
import utils.actions
from utils.dirs import ApplyToDirs,ApplyToFiles

NEG_VALUE=100
POZ_VALUE=200

@ApplyToFiles(dir_arg=True)
def action_diff(in_path,out_path):
    print(str(out_path))
    action_i=utils.actions.read_action(in_path,False)
    new_frames=action_i.apply_temporal(encode)
    new_action=utils.actions.Action(action_i.name,new_frames)
    new_action.save(out_path)

@ApplyToDirs()
def diff(in_path,out_path):
    img=cv2.imread(str(in_path))
    img=smooth_diff(img)
    cv2.imwrite(str(out_path),img)

def encode(img1,img2):
    img1=standarize(img1,mult=15.0,trans=0.0)
    img2=standarize(img2,mult=15.0,trans=0.0)
    img2*=16.0
    #img2+=15.0
    img3=img1+img2
    img3=np.sqrt(img3)
    print(np.max(img1))
    print(np.max(img2))
    print(np.max(img3))
    return img3

def smooth_diff2(img1,img2):
    img1=clean(img1)
    img2=clean(img2)
    img3=img2-img1
    img3=sign_diff(img3)
    return img3

def clean(img):
    img = cv2.medianBlur(img,5)
    img=img.astype(float)
    return img

def unify_img(img,diff):
    img=standarize(img)
    poz_val=np.max(diff)
    neg_val=np.min(diff[diff!=0])
    threshold=(poz_val+neg_val)/2.0
    diff2=np.zeros(diff.shape)
    diff2[diff!=0]=50
    diff2[diff>threshold]=250
    select=(diff!=0)
    img[select]=diff2[select]
    return img

def smooth_diff(img):
    img = cv2.medianBlur(img,5)
    img=img.astype(float)
    diff=basic_diff(img)
    print(img.shape)
    print(diff.shape)
    diff=sign_diff(diff)
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

def standarize(img,mult=128.0,trans=64):
    img=img.astype(float)
    max_value=np.max(img)
    min_value=np.min(img[img!=0])
    img[img!=0]-=(min_value-1.0)
    delta=np.max(img)#max_value-min_value+1.0
    img/=delta
    img[...]*=mult #128.0
    img[img!=0]+=trans#64.0
    return img

def sign_diff(img):
    #img=basic_diff(img)
    img[img>0]=POZ_VALUE
    img[img<0]=NEG_VALUE
    return img

def full_diff(img):
    img=basic_diff(img)
    return np.abs(img)

def simple_diff(img1,img2):
    return img1

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