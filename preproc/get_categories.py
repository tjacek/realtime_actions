import utils.files as files
import re

def extract(path):
    txt=files.read_file(path)
    txt=files.array_to_txt(txt)
    print(txt)
    pattern = re.compile(r"s\d+_e\d+\n")
    actions=pattern.split(txt)
    cats=[parse_action(action_i) for action_i in actions
                                if action_i!='']
    print(cats)

def parse_action(raw_action):
    cats={}
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

