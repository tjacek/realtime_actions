import utils.files as files
import re

class Action(object):
    def __init__(self,name):
    	self.name=name
        self.data={}

    def __getitem__(self,index):
       return self.data[index]

    def __setitem__(self,index,value):
        self.data[index]=value

    def __str__(self):
        return self.name     	

def extract(path):
    txt=files.read_file(path)
    txt=files.array_to_txt(txt)
    print(txt)
    pattern = re.compile(r"s\d+_e\d+\n")
    action_names=re.findall(pattern, txt)
    actions=pattern.split(txt)
    cats=[parse_action(name_i,action_i) for name_i,action_i in zip(action_names,actions)
                                if action_i!='']
    print(cats[0])

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

