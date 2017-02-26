import sys,os
sys.path.append(os.path.abspath('../cluster_images'))
#import scipy.io as sio
import numpy as np
import h5py
import utils.dirs
import utils.imgs

import cv2

@utils.dirs.ApplyToFiles()
def from_mat(action_path,out_path):
    print(action_path)
    action_dataset=get_action_dataset(action_path)
    time_dim=get_time_dim(action_dataset)
    action_name=action_path.get_name()
    utils.dirs.make_dir(out_path)
    for i in range(time_dim-1):     
        #frame_i=standarize(frame_i)
        name=action_name.replace('.mat',str(i)+".jpg")
        print(str(out_path))
        full_path=out_path+name
        print(str(full_path))
        frame_i=get_frame(i,action_dataset)
        cv2.imwrite(str(full_path),frame_i)

def get_action_dataset(action_path):
    #print(action_name)
    action_file=h5py.File(str(action_path),'r')
    action_dataset=action_file['cropped_depth']
    return action_dataset

def get_time_dim(action_dataset):
    return action_dataset.shape[0]

def get_frame(i,action_dataset):
    frame_i=action_dataset[i,:,:]
    frame_i=frame_i.T
    frame_i=standarize(frame_i)
    print(np.amax(frame_i))
    return	frame_i

def standarize(img,mult=128.0,trans=64):
    max_value=np.max(img)
    min_value=np.min(img[img!=0])
    img[img!=0]-=(min_value-1.0)
    delta=np.max(img)#max_value-min_value+1.0
    img/=delta
    img[...]*=mult #128.0
    img[img!=0]+=trans#64.0
    return img

def is_file(item):
    return isinstance(item, h5py.File)

if __name__ == "__main__":
    from_mat("../dataset3/preproc/raw","../dataset3/preproc/depth_")