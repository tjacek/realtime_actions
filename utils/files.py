import os
import os.path as io 
import pickle,re 
from natsort import natsorted
from shutil import copyfile

def get_files(path):
    all_in_dir=os.listdir(path)
    files= [f for f in all_in_dir  
              if is_file(f,path)]
    files=natsorted(files)#files.sort()
    return files

def get_dirs(path):
    all_in_dir=os.listdir(path)
    files= [f for f in all_in_dir  
              if not is_file(f,path)]
    files=natsorted(files)#files.sort()
    return files

def get_paths(path):
    names=get_files(path)
    return append_path(path,names)

def conversion(in_path,out_path,conv,dir=True):
    make_dir(out_path)
    if(dir):
        paths=get_files(in_path)
    else:
        paths=get_dirs(in_path)
    print(in_path)
    print(paths)
    in_paths=append_path(in_path,paths)
    out_paths=append_path(out_path,paths)
    for in_i,out_i in zip(in_paths,out_paths):
        print(in_i)
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
        for j,img_i in enumerate(img_names):
            src=in_i+"/"+img_i
            dst=out_path+"/"+img_i
            postfix="_"+str(i)+"_" + str(j) +".jpg"
            dst=dst.replace(".jpg",postfix)
            print(src)
            print(dst)
            copyfile(src, dst)

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

def replace_sufix(sufix,files):
    return map(lambda s:s.replace(sufix,""),files)

def extract_prefix(filename):
    return filename.split(".")[-1]

def rename(in_paths,out_paths):
    for in_i,out_i in zip(in_paths,out_paths):
        os.rename(in_i,out_i)

def extract_number(path):
    name=get_name(path)
    pattern = re.compile(r"\d+")
    raw_digits=re.findall(pattern,name)[0]
    return int(raw_digits)

def replace_path(old_path, new_path):
    name=get_name(old_path)
    return new_path+"/"+name