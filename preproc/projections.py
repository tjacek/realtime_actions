import sys,os
sys.path.append(os.path.abspath('../realtime_actions'))
import numpy as np
import cv2
import utils.dirs
import utils.imgs

ONE=100.0

@utils.dirs.apply_to_files
def apply_projection(in_path,out_path):
    img_i=utils.imgs.read_raw(in_path)
    proj_img=project_img(img_i)
    cv2.imwrite(str(out_path),proj_img)

def project_img(img):
    img_xy=proj_xy(img)
    img_zy=proj_xy(img)
    img_xz=proj_xy(img)
    proj_img=np.concatenate([img_xy,img_zy,img_xy])
    return proj_img

def proj_xy(img):
    img_xy=np.zeros(img.shape)
    for (x_i, y_i), element in np.ndenumerate(img):
        if(element!=0):
            img_xy[x_i][y_i]=ONE
    return img_xy    
    
if __name__ == "__main__":
    in_path='../dataset0/bounded'
    out_path='../dataset0/proj'
    apply_projection(in_path,out_path)