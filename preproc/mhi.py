import numpy as np 
import utils.actions 
from utils.dirs import ApplyToDirs,ApplyToFiles

@ApplyToFiles(dir_arg=True)
def action_mhi(in_path,out_path):
    action_i=utils.actions.read_action(in_path,False)	
    diff_action=action_i.transform_action(threshold_diff)
    mhi=[np.zeros(action_i.orginal_dim(0))]
    diff_frames=diff_action.orginal_imgs()
    for diff_t in diff_frames:
        mhi_next=motion_history(mhi[-1],diff_t)
        mhi.append(mhi_next)
    img=action_i.numpy_to_img(mhi)
    mhi_action=utils.actions.Action(action_i.name,img)
    mhi_action.save(out_path)

def motion_history(mhi_t0,b_t,tau=5.0):
    mhi_t1=np.zeros(mhi_t0.shape)
    mhi_t1[b_t!=0]=tau
    mhi_t1[b_t==0]=mhi_t0[b_t==0]-1
    mhi_t1[0>mhi_t1]=0
    mhi_t1*=10
    return mhi_t1

def threshold_diff(img1,img2,threshold=10):
    diff_img=simple_diff(img1,img2)
    diff_img[diff_img<threshold]=0
    diff_img[diff_img!=0]=1
    return diff_img

def simple_diff(img1,img2):
    img3=img1-img2
    return np.abs(img3)

