import numpy as np
import cv2
import utils.actions
import utils.imgs
import utils.dirs
from utils.dirs import dir_arg,file_dec, ApplyToFiles, ApplyToDirs

@ApplyToFiles(dir_arg=True)
def bound_action(action_path,out_path):
    print(out_path)
    utils.dirs.make_dir(out_path)
    action=utils.actions.read_action(action_path,False)
    new_imgs=action.apply_temporal(extract_box)
    [utils.imgs.save_img(out_path,img_i) for img_i in new_imgs]

@ApplyToDirs()
def bound_img(in_path,out_path):
    print("$$$$$$$$$$$$")
    print(str(in_path))
    img_i=utils.imgs.read_raw(in_path)
    p1,p2=simple_bbox(img_i)
    print(p1)
    print(p2)
    bound_img=slice_img(p1,p2,img_i)
    cv2.imwrite(str(out_path),bound_img)

def extract_box(img1,img2):
    org_img1=img1.get_orginal()
    org_img2=img2.get_orginal()
    p1,p2=moving_bbox(org_img1,org_img2)
    new_img1=org_img1[p1[0]:p2[0],p1[1]:p2[1]]
    new_img2=org_img2[p1[0]:p2[0],p1[1]:p2[1]]
    concat_img=np.concatenate((new_img1,new_img2))
    return utils.imgs.Image(img1.name,concat_img)

def moving_bbox(img1,img2):
    points=[]
    points+=simple_bbox(img1)
    points+=simple_bbox(img2)
    points=np.array(points)
    x_dim=points[:,0]
    y_dim=points[:,1]
    return (min(y_dim),min(x_dim)),(max(y_dim),max(x_dim)) 

def simple_bbox(img):
    print(img.shape)
    img=img.astype(np.uint8)
    x0,y0,w,h=cv2.boundingRect(img)
    return [(x0,y0),((x0+w,y0+h))] 

def slice_img(p1,p2,img_i):
    return img_i[p1[1]:p2[1],p1[0]:p2[0]]

if __name__ == "__main__":
    img1=read_raw("in1.jpg")
    img2=read_raw("in2.jpg")
    new_img=extract_box(img1,img2)
    cv2.imwrite("out.jpg",new_img)