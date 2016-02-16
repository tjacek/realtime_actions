import utils.files as files
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

    def get_path(self,in_path):
        return in_path+"/"+self.name

    def get_frame_names(self,in_path):
        full_path=self.get_path(in_path)
        names_only=files.get_files(full_path)
        frame_names=[ self.name+"/"+name_i for name_i in names_only]
        #print(frame_names)
        return files.append_path(in_path,frame_names) 

    def categorize(self,frame_names):
        cats=[self.get_category(name_i) for name_i in frame_names]
        return zip(frame_names,cats)

    def get_category(self,frame_name):
        id=files.extract_number(frame_name)
        for cat_i in self.data.keys():
            a,b=self.data[cat_i]
            if( a<=id and id<=b):
                return cat_i
        return None

def extract(action_path,out_path,cat_path):
    txt=files.read_file(cat_path)
    txt=files.array_to_txt(txt)
    print(txt)
    pattern = re.compile(r"s\d+_e\d+\n")
    action_names=re.findall(pattern, txt)
    actions=pattern.split(txt)
    actions=[parse_action(name_i,action_i) 
             for name_i,action_i in zip(action_names,actions)
                                if action_i!='']
    
    [seg_action(action_path,out_path,act_i) for act_i in actions]

def seg_action(action_path,out_path,action):
    files.make_dir(out_path)
    frame_names=action.get_frame_names(action_path)
    print(frame_names)
    cats=action.categorize(frame_names)
    print(cats)
    cats=[ (frame_path,cat_i) for frame_path,cat_i in cats
                                if cat_i!=None]
    for frame_path,cat_i in cats:
        print(frame_path)
        cat_path=out_path+"/"+cat_i
        files.make_dir(cat_path)
        instance_path=cat_path+"/"+action.name
        files.make_dir(instance_path)
        full_path=files.replace_path(frame_path,instance_path)
        print(full_path)
        copyfile(frame_path, full_path)
    return len(cats)

def parse_action(name,raw_action):
    cats=Action(name)
    raw_cats=[parse_line(line) for line in raw_action.split("\n")]
    for ln in raw_cats:
        if(ln!=None):
            cats[ln[0]]=ln[1]
    return cats

def parse_line(line):
    raw=line.split(" ")
    print(raw)
    if(len(raw)==3):
        name=raw[0].replace(":","")
        a=int(raw[1])
        b=int(raw[2])
        return name,(a,b)
    return None
