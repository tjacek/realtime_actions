import cv2
import numpy as np
import utils.actions
import utils.imgs

def detect_edges(in_path,out_path):
    img=cv2.imread(in_path,cv2.IMREAD_GRAYSCALE)
    kernel = np.ones((9,9),np.float32)/25
    img = cv2.filter2D(img,-1,kernel)
    img=cv2.Canny(img,1,255)
    cv2.imwrite(out_path,img)

@utils.actions.action_dec
def rescale(img,new_dim=(60,120)):
    raw_img=img.get_orginal()
    new_img = cv2.resize(raw_img,new_dim, interpolation = cv2.INTER_CUBIC)
    return utils.imgs.Image(img.name,new_img) 
 
