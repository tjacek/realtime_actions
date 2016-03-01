import utils.files as files
import utils.text as text
from shutil import copyfile
import re

class Action(object):
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
        frame_names=self.get_frame_names(action_path)
        cats=[self.get_category(name_i) for name_i in frame_names]
        cat_frames=zip(frame_names,cats)
        cat_frames=[ (frame_path,cat_i) for frame_path,cat_i in cat_frames
                                if cat_i!=None]
        return cat_frames

    def get_category(self,frame_name):
        id=text.extract_number(frame_name)
        for cat_i in self.data.keys():
            a,b=self.data[cat_i]
            if( a<=id and id<=b):
                return cat_i
        return None

    def get_path(self,in_path):
        return in_path+"/"+self.name

    def get_frame_names(self,in_path):
        full_path=self.get_path(in_path)
        return files.get_files(full_path,True)

def extract(action_path,out_path,cat_path):
    actions_info=parse_info(cat_path)
    actions=[parse_action(name_i,action_i) 
             for name_i,action_i in actions_info
                                if action_i!='']
    print(actions_info)
    [seg_action(action_path,out_path,act_i) for act_i in actions]

def parse_info(cat_path):
    txt=files.read_file(cat_path)
    txt=files.array_to_txt(txt)
    pattern = re.compile(r"s\d+_e\d+\n")
    action_names=re.findall(pattern, txt)
    actions=pattern.split(txt)
    del actions[0]
    return zip(action_names,actions)

def seg_action(action_path,out_path,action):
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
    #print(action)
    files.make_dir(out_path)
    cats=action.categorize(action_path)
    for frame_path,cat_i in cats:
         print(frame_path)
         cat_path=out_path+"/"+cat_i
         files.make_dir(cat_path)
         instance_path=cat_path+"/"+action.name
         files.make_dir(instance_path)
         dst_path=files.replace_path(frame_path,instance_path)
         print(dst_path)    
         copyfile(frame_path, dst_path)
    return len(cats)

def parse_action(name,raw_action):
    action=Action(name)
    raw_cats=[parse_line(line) for line in raw_action.split("\n")]
    for ln in raw_cats:
        if(ln!=None):
            action[ln[0]]=ln[1]
    return action

def parse_line(line):
    raw=line.split(" ")
    print(raw)
    if(len(raw)==3):
        name=raw[0].replace(":","")
        a=int(raw[1])
        b=int(raw[2])
        return name,(a,b)
    return None