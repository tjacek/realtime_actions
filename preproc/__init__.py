import cv2
import numpy as np
import utils.actions
import utils.imgs
from utils.dirs import ApplyToDirs,ApplyToFiles

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

@ApplyToFiles(dir_arg=True)
def median_action(action_path,out_path,k=3):
    action=utils.actions.read_action(action_path)
    def median_subseq(i):
        low=i-k
        high=i+k
        if(low<0):
            low=0
        seq_i=np.array(action.frames[low:high])
        seq_i=seq_i.reshape((seq_i.shape[0],seq_i.shape[2]))
        med_i=np.median(seq_i,axis=0)
        print(type(med_i))
        return med_i
    med_arr=[]
    for i in range(len(action)):
        seq_i= median_subseq(i)	
        org_dim=action.frames[i].org_dim
        name=action.frames[i].name
        seq_i=seq_i.reshape(org_dim)
        img_i=utils.imgs.Image(name,seq_i)
        med_arr.append(img_i)
    action.frames=med_arr
    action.save(out_path)

@ApplyToFiles(dir_arg=True)
def unify_actions(in_path1,in_path2):
    out_path=in_path2.copy()
    out_path.pop()
    out_path.set_name("unify")
    utils.dirs.make_dir(out_path)
    print(str(in_path1))
    print(str(in_path2))
    print(str(out_path))
    action1=utils.actions.read_action(in_path1,False)
    action2=utils.actions.read_action(in_path2,False)
    imgs1=action1.orginal_imgs()
    imgs2=action2.orginal_imgs()
    new_frames=[img1_i-img1_i for img1_i,img2_i 
                 in zip(imgs1,imgs2)]
    def new_img(i,img_i):
    	name_i=action1.frames[i].name
    	return utils.imgs.Image(name_i,img_i)
    new_frames=[ new_img(i,img_i)
          for i,img_i in enumerate(new_frames)]
    new_action=utils.actions.Action(action1.name,new_frames)
    new_action.save(out_path.create(new_action.name))