import os
import os.path as io 
import pickle,re 

def get_files(path):
    all_in_dir=os.listdir(path)
    files= [f for f in all_in_dir  
              if is_file(f,path)]
    files.sort()
    return files

def get_dirs(path):
    all_in_dir=os.listdir(path)
    files= [f for f in all_in_dir  
              if is_file(f,path)]
    dirs.sort()
    return dirs

def read_file(path):
    file_object = open(path,'r')
    lines=file_object.readlines()  
    file_object.close()
    return lines

def is_file(f,path):
        return io.isfile(io.join(path,f))

def make_dir(path):
    if(not os.path.isdir(path)):
        os.system("mkdir "+path)

def get_name(path):
    return path.split("/")[-1]

def array_to_txt(array):
    return "".join(array)

def save_object(nn,path):
    file_object = open(path,'wb')
    pickle.dump(nn,file_object)
    file_object.close()

def save_string(path,string):
    file_str = open(path,'w')
    file_str.write(string)
    file_str.close()

def read_object(path):
    file_object = open(path,'r')
    obj=pickle.load(file_object)  
    file_object.close()
    return obj

def append_path(path,files):
    paths=[path+"/"+f for f in files]
    paths=[path.replace("//","/") for path in paths]
    return paths

def replace_sufix(sufix,files):
    return map(lambda s:s.replace(sufix,""),files)

def extract_prefix(filename):
    return filename.split(".")[-1]	