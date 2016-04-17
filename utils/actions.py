import files,dirs
import cv2
import numpy as np
import utils.imgs as imgs
from utils.paths import path_args
from dirs import ApplyToFiles

class Action(object):
    def __init__(self,name,frames,cat=None):
        self.name=name
        self.frames=[frame_i.flat2D() for frame_i in frames]
        self.cat=cat
        self.seq=None
    
    def __str__(self):
    	return self.name

    def __getitem__(self,index):
        return self.frames[index]

    def __len__(self):
        return len(self.frames)

    def apply(self,fun):
        return [ fun(frame_i) for frame_i in self.frames]

    def apply_temporal(self,fun):
        img_range=range(len(self)-1)
        items=self.frames
        return [fun(items[i],items[i+1]) for i in img_range]

    def as_numpy(self):
        return np.array(self.frames)

    def cat_labels(self):
        return [(frame_i,self.cat) for frame_i in self.frames]

def action_dec(func):
    @ApplyToFiles(dir_arg=True)
    def transform_action(action_path,out_path):
        print(out_path)
        dirs.make_dir(out_path)
        action=read_action(action_path,False)
        new_imgs=action.apply(func)
        [imgs.save_img(out_path,img_i) for img_i in new_imgs]
    return transform_action


@path_args
def read_action(action_path,print_action=True):
    frames= imgs.read_images(action_path)
    if(frames==None):
        return None
    if(len(frames)==0):
        return None
    name=action_path.get_name()
    cat=dir_cat(action_path,name)
    if(print_action):
        print(action_path)
        print("name: "+name)
        print("category:" + str(cat))
        print(len(frames))
    return Action(name,frames,cat)

def apply_to_actions(actions,fun):
    all_actions=[]
    for action_i in actions:
        all_actions+=action_i.apply(fun)
    return all_actions

def dir_cat(action_path,name):
    return action_path.items[-2]