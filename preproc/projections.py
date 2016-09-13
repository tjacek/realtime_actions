import sys,os
sys.path.append(os.path.abspath('../realtime_actions'))
import numpy as np
import cv2
import utils.dirs
import utils.imgs

ONE=200.0

@utils.dirs.apply_to_files
def apply_projection(in_path,out_path):
    img_i=utils.imgs.read_raw(in_path)
    proj_img=project_img(img_i)
    cv2.imwrite(str(out_path),proj_img)

def project_img(img,new_dim=(60,60)):
    img_xy=proj_xy(img)
    img_zy=proj_zy(img)
    img_xz=proj_xz(img)
    all_imgs=[img_xy,img_zy,img_xz]
    all_imgs=[ clean(img_i) for img_i in all_imgs]
    all_imgs=[ cv2.resize(img_i,new_dim, interpolation = cv2.INTER_CUBIC)
                for img_i in all_imgs]
    proj_img=np.concatenate(all_imgs)
    return proj_img

def proj_xy(img):
    img_xy=np.zeros(img.shape)
    for (x_i, y_i), element in np.ndenumerate(img):
        if(element!=0):
            img_xy[x_i][y_i]=ONE
    return img_xy    

def proj_zy(img):
    max_z=np.amax(img)
    zy_shape=(img.shape[0],max_z+3)
    img_zy=np.zeros(zy_shape)
    for (x_i, y_i), element in np.ndenumerate(img):
        if(element!=0):
            img_zy[x_i][int(element)]=ONE
    return img_zy

def proj_xz(img):
    max_z=np.amax(img)
    zy_shape=(max_z+3,img.shape[1])
    img_zy=np.zeros(zy_shape)
    for (x_i, y_i), element in np.ndenumerate(img):
        if(element!=0):
            img_zy[int(element)][y_i]=ONE
    return img_zy

def clean(raw_img):
    smooth_img=cv2.blur(raw_img,(5,5))
    smooth_img=smooth_img.astype(np.uint8)
    ret,binary_img=cv2.threshold(smooth_img,1,255,cv2.THRESH_BINARY)
    return binary_img

if __name__ == "__main__":
    in_path='../dataset0/bounded'
    out_path='../dataset0/proj'
    apply_projection(in_path,out_path)