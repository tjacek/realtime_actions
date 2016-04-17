import utils.dirs as dirs
import utils.files as files
import utils.text as text
from shutil import copyfile
import re
from utils.paths import path_args,str_arg

class ActionDict(object):
    def __init__(self,name):
    	self.name=name.replace("\n","")
        self.data={}

    def __getitem__(self,index):
       return self.data[index]

    def __setitem__(self,index,value):
        self.data[index]=value

    def __str__(self):
        return self.name

    def categorize(self,action_path):
        print("&&&&&&&&&&&&&&&&&&&&")
        frame_names=dirs.get_files(action_path,dirs=False)
        cats=[self.get_category(name_i) for name_i in frame_names]
        cat_frames=zip(frame_names,cats)
        cat_frames=[ (frame_path,cat_i) for frame_path,cat_i in cat_frames
                                if cat_i!=None]
        return cat_frames

    def get_category(self,frame_name):
        print(str(frame_name))
        id=text.extract_number(frame_name)
        for cat_i in self.data.keys():
            a,b=self.data[cat_i]
            if( a<=id and id<=b):
                return cat_i
        return None
    
    @path_args
    def get_path(self,in_path):
        return in_path.append(self.name)

    def get_frame_names(self,in_path):
        full_path=self.get_path(in_path)
        return dirs.get_files(full_path)

@path_args
def extract(action_path,out_path,cat_path):
    actions_info=parse_info(cat_path)
    actions=[parse_action(name_i,action_i) 
             for name_i,action_i in actions_info
                                if action_i!='']
    
    print(actions[0].name)
    [seg_action(action_path,out_path,act_i) for act_i in actions]

@str_arg
def parse_info(cat_path):
    txt=files.read_file(cat_path)
    txt=files.array_to_txt(txt)
    pattern = re.compile(r"s\d+_e\d+\n")
    action_names=re.findall(pattern, txt)
    actions=pattern.split(txt)
    del actions[0]
    return zip(action_names,actions)

def seg_action(action_path,out_path,action_dict):
    action_path=action_path.create(action_dict.name)
    out_path=out_path.create(action_dict.name)
    cats=action_dict.categorize(action_path)
    cat_dict={}
    for cat_i in action_dict.data.keys():
        cat_path=out_path.copy()
        cat_path.set_name(cat_i)
        dirs.make_dir(cat_path)
        cat_dict[cat_i]=cat_path 
    for frame_path,cat_i in cats:
        dst_path=cat_dict[cat_i]
        dst_path=dst_path.create(action_dict.name)
        dirs.make_dir(dst_path)
        dst_path=dst_path.replace(frame_path)
        print(frame_path)
        print(dst_path)
        copyfile(str(frame_path), str(dst_path))

def parse_action(name,raw_action):
    action=ActionDict(name)
    raw_cats=[parse_line(line) for line in raw_action.split("\n")]
    for ln in raw_cats:
        if(ln!=None):
            action[ln[0]]=ln[1]
    return action

def parse_line(line):
    raw=line.split(" ")
    if(len(raw)==3):
        name=raw[0].replace(":","")
        a=int(raw[1])
        b=int(raw[2])
        return name,(a,b)
    return None