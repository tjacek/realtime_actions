import utils.text as text
import os
import os.path as io 
import pickle,re 
import shutil
from natsort import natsorted
from shutil import copyfile

def get_files(path,append=False):
    all_in_dir=os.listdir(path)
    files= [f for f in all_in_dir  
              if is_file(f,path)]
    files=natsorted(files)
    if(append_path):
        files=append_path(path,files)
    return files

def get_dirs(path,append=False):
    all_in_dir=os.listdir(path)
    files= [f for f in all_in_dir  
              if not is_file(f,path)]
    files=natsorted(files)#files.sort()
    if(append_path):
        files=append_path(path,files)
    return files

def get_paths(path):
    names=get_files(path)
    return append_path(path,names)

def dir_conversion(in_path,out_path,conv):
    def files_conversion(in_path,out_path):
        conversion(in_path,out_path,conv)
    conversion(in_path,out_path,files_conversion,False)

def conversion(in_path,out_path,conv,dir=True):
    make_dir(out_path)
    if(dir):
        in_paths=get_files(in_path,True)
    else:
        in_paths=get_dirs(in_path,True)
    
    out_paths=[ replace_path(in_path_i,out_path) for in_path_i in in_paths]
    for in_i,out_i in zip(in_paths,out_paths):
        print(in_i)
        print(out_i)
        conv(in_i,out_i)

def dir_to_txt(in_path,out_path):
    dir_content=get_files(in_path)
    dir_paths=append_path(in_path,dir_content)
    text="\n".join(dir_paths)
    save_string(out_path,text)
    return dir_content

def unify_dir(in_path,out_path):
    make_dir(out_path)
    paths=get_dirs(in_path)
    in_paths=append_path(in_path,paths)
    for i,in_i in enumerate(in_paths):
        img_names=get_files(in_i)
        #print(img_names)
        for j,img_i in enumerate(img_names):
            src=img_i#in_i+"/"+img_i
            print(src)
            dst=out_path+"/"+get_name(img_i)
            postfix="_"+str(i)+"_" + str(j) +".jpg"
            dst=dst.replace(".jpg",postfix)
            print(src)
            print(dst)
            copyfile(src, dst)

def flatten_dir(in_path,out_path):
    make_dir(out_path)
    all_dirs=get_dirs(in_path,True)
    old_files=get_files(in_path,True)
    new_files=[replace_path(file_i,out_path) for file_i in old_files]
    for in_i,out_i in zip(old_files,new_files):
        print(in_i)
        print(out_i)
        shutil.move(in_i,out_i)
    for dir_i in all_dirs:
        flatten_dir(dir_i,out_path)

def extract_dir(in_path,out_path,sufix="pcd"):
    make_dir(out_path)
    filenames=get_files(in_path)
    filenames=[filename_i for filename_i in filenames
                        if text.has_sufix(filename_i,sufix)]
    for filename_i in filenames:
        shutil.move(in_path+"/"+filename_i,out_path+"/"+filename_i)

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
    return objh

def append_path(path,files):
    paths=[path+"/"+f for f in files]
    paths=[path.replace("//","/") for path in paths]
    return paths

def rename(in_paths,out_paths):
    for in_i,out_i in zip(in_paths,out_paths):
        os.rename(in_i,out_i)

def replace_path(old_path, new_path):
    name=get_name(old_path)
    return new_path+"/"+name