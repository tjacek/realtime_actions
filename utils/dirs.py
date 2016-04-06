import os
import os.path as io 
import paths
from natsort import natsorted
from shutil import copyfile

def copy_dir(in_path,out_path):
    in_files=get_files(in_path,dirs=False)
    print(in_files)
    for in_file_i in in_files:
    	#out_file_i=in_file_i.replace(out_path)
        print(type(out_path))#out_file=out_path.

def get_files(dir_path,dirs=True,append_path=True):
    d_path=str(dir_path)
    all_in_dir=os.listdir(d_path)
    print(all_in_dir)
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
    print(file_path)
    return io.isfile(file_path)#io.join(path,f))

def make_dir(path):
    if(not os.path.isdir(path)):
        os.system("mkdir "+path)

if __name__ == "__main__":
    data="../../dataset6/imgs"
    copy_dir(data,"test")
    