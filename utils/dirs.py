import os
import os.path as io 
import paths 
from natsort import natsorted
from shutil import copyfile
from sets import Set

def apply_to_files(func):
    @paths.path_args
    def inner_func(*args):
        old_path=str(args[0])
        new_path=str(args[1])
        other_args=args[2:]
        in_paths=all_files(old_path)
        out_paths=[path_i.exchange(old_path,new_path) 
                      for path_i in in_paths]
        make_dirs(new_path,out_paths)              
        for in_i,out_i in zip(in_paths,out_paths):
            func(in_i,out_i,*other_args)
    return inner_func    

def apply_to_dirs( func):    
    @paths.path_args
    def inner_func(*args):
        old_path=str(args[0])
        new_path=str(args[1])
        other_args=args[2:]
        in_paths=bottom_dirs(old_path)
        out_paths=[path_i.exchange(old_path,new_path) 
                      for path_i in in_paths]
        make_dirs(new_path,out_paths)              
        for in_i,out_i in zip(in_paths,out_paths):
            func(in_i,out_i,*other_args)
    return inner_func

def dir_arg(func):
    def inner_func(dir_path):
        dirs=get_files(dir_path,dirs=False)
        return func(dirs)
    return inner_func

def file_dec(func):
    @paths.path_args
    def inner_func(dir_path):
        file_paths=get_files(dir_path,dirs=False)
        return [func(file_i) for file_i in file_paths]
    return inner_func

@paths.path_args
def copy_dir(in_path,out_path):
    in_files=get_files(in_path,dirs=True)
    make_dir(str(out_path))
    for in_file_i in in_files:
        out_file_i=out_path.replace(in_file_i)
        make_dir(str(out_file_i))
        print(str(in_file_i))
        print(str(out_file_i))#out_file=out_path.
        unify_dirs(str(in_file_i),str(out_file_i)) 

@paths.path_args
def unify_dirs(in_path,out_path):
    dirs_paths=get_files(in_path)
    make_dir(str(out_path))
    files_paths=[]
    for dir_i in dirs_paths:
        files_paths+=get_files(dir_i,dirs=False)
    for in_file_i in files_paths:
        print(str(in_file_i))
        out_file_i=out_path.replace(in_file_i)
        print(str(out_file_i))
        copyfile(str(in_file_i),str(out_file_i))

def get_files(dir_path,dirs=True,append_path=True):
    d_path=str(dir_path)
    all_in_dir=os.listdir(d_path)
    if(dirs):    
        files= [f for f in all_in_dir  
                 if (not is_file(f,dir_path))]
    else:
        files= [f for f in all_in_dir  
                 if is_file(f,dir_path)]
    files=natsorted(files)
    if(append_path):
        files=[paths.get_paths(dir_path,file_i) for file_i in files]
    return files

def is_file(f,path):
    file_path=str(path)+"/"+f
    return io.isfile(file_path)#io.join(path,f))

@paths.str_arg
def make_dir(path):
    if(not os.path.isdir(path)):
        os.system("mkdir "+path)

def all_files(in_path):
    dirs_i=get_files(in_path,dirs=True)
    files_i=get_files(in_path,dirs=False)
    if(dirs_i):
        for dirs_ij in dirs_i:
            files_i+=all_files(dirs_ij)
    return files_i

def bottom_dirs(in_path):
    dirs_i=get_files(in_path,dirs=True)
    bottom=[]
    if(dirs_i):
        for dirs_ij in dirs_i:
            bottom+=bottom_dirs(dirs_ij)
    else:
        bottom.append(in_path)
    return bottom

def make_dirs(out_path,dirs):
    all_dirs=Set()
    bottom_dirs=Set([str(dir_i) for dir_i in dirs])
    for dir_i in dirs:
        postfix=str(dir_i).replace(out_path,'')
        postfix=postfix.split('/')
        paths_i=sub_paths(out_path,dir_i)
        all_dirs.update(paths_i)
    make_dir(out_path)
    for dir_i in all_dirs:
        if(not dir_i in bottom_dirs):
            make_dir(dir_i)

def sub_paths(out_path,dirs):
    dir_path=[] 
    sub_paths=[]
    for dir_i in dirs:
        sub_path_i=dir_path + [dir_i]
        sub_paths.append('/'.join(sub_path_i))
        dir_path=sub_path_i
    return sub_paths   
if __name__ == "__main__":
    path="../../dataset9/"
    unify_dirs(path+"final/",path+"imgs/")
    #unify_dirs(data,"test2")
    