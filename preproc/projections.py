import sys,os
sys.path.append(os.path.abspath('../realtime_actions'))
import numpy as np
import cv2
import utils.dirs
import utils.imgs

ONE=80.0

@utils.dirs.apply_to_files
def apply_projection(in_path,out_path):
    print(str(in_path))
    img_i=utils.imgs.read_raw(in_path)
    #ret,filtr_img=cv2.threshold(img_i,5,255,cv2.THRESH_BINARY)
    proj_img=project_img(img_i)
    cv2.imwrite(str(out_path),proj_img)

def project_img(img,new_dim=(60,60),xy_proj=False):
    #img_xy=proj_xy(img)
    img_zy=proj_zy(img)
    img_xz=proj_xz(img)
    all_imgs=[img_zy,img_xz] #img_xy]
    all_imgs=[ clean(img_i) for img_i in all_imgs]
    if(xy_proj):
        all_imgs.append(proj_xy(img))
    else:
        all_imgs.append(img)
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
    print(max_z)
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
    smooth_img=cv2.blur(raw_img,(3,3))
    smooth_img=smooth_img.astype(np.uint8)
    ret,binary_img=cv2.threshold(smooth_img,1,255,cv2.THRESH_BINARY)
    binary_img[binary_img!=0]=ONE
    return binary_img

if __name__ == "__main__":
    in_path='../dane4/scaled'
    out_path='../dane4/proj'
    apply_projection(in_path,out_path)