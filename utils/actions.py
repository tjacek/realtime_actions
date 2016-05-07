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
    
    def orginal_imgs(self):
        return [frame_i.get_orginal() for frame_i in self.frames]

    def orginal_dim(self,i):
        return self.frames[i].org_dim

    def apply(self,fun):
        return [ fun(frame_i) for frame_i in self.frames]

    def transform_action(self,fun):
        new_frames=self.apply_temporal(fun)
        return Action(self.name,new_frames)

    def apply_temporal(self,fun):
        img_range=range(len(self)-1)
        items=self.orginal_imgs()#self.frames
        raw_imgs=[fun(items[i],items[i+1]) for i in img_range]
        return [ imgs.Image(self.frames[i].name,img_i) 
                   for i,img_i in enumerate(raw_imgs)]

    def numpy_to_img(self,raw_imgs):
        return [ imgs.Image(frame_i.name,img_i,frame_i.org_dim) 
                  for frame_i,img_i in zip(self.frames,raw_imgs)]
   
    def as_numpy(self):
        return np.array(self.frames)

    def cat_labels(self):
        return [(frame_i,self.cat) for frame_i in self.frames]

    def save(self,out_path):
        print(str(out_path))
        dirs.make_dir(out_path)
        [imgs.save_img(out_path,img_i) for img_i in self.frames]

    def all_names(self):
        return [name_i for frame_i in self.frames]

def action_dec(func):
    @ApplyToFiles(dir_arg=True)
    def transform_action(action_path,out_path):
        print(out_path)
        dirs.make_dir(out_path)
        action=read_action(action_path,False)
        new_imgs=action.apply(func)
        [imgs.save_img(out_path,img_i) for img_i in self.frames]
    return transform_action

@path_args
def read_action(action_path,print_action=True):
    frames= imgs.read_images(action_path)
    if(frames==None):
        return None
    if(len(frames)==0):
        return None
    name=action_path.get_name()
    cat=name_cat(action_path,name)#dir_cat(action_path,name)
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

def name_cat(action_path,name):
    return name.split("_")[0]

@path_args
def action_cats(action_path,out_path):
    dirs.make_dir(out_path)
    action_paths=dirs.get_files(action_path,dirs=True)
    actions=[ read_action(path_i,False) for path_i in action_paths]
    cats={}
    for action_i in actions:
        cats[action_i.cat]=out_path.create(action_i.cat)
    for cat_i in cats.keys():
        dirs.make_dir(cats[cat_i])
    for action_i in actions:
        name=action_i.name
        cat_path=cats[action_i.cat]
        dst_path=cat_path.create(name)
        print(str(dst_path))
        action_i.save(dst_path)
        