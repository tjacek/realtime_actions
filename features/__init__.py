import utils 
import utils.files
import os
from shutil import copyfile

def extract_features(in_path,out_path):
    cat_dirs=utils.files.get_dirs(in_path,True)
    for cat_i in cat_dirs:
        convert_dir(cat_i,out_path)
    #utils.files.conversion(in_path,out_path,convert_dir)

def convert_dir(in_path,out_path):
    print(in_path)
    out_path=get_outpath(in_path,out_path)
    print(out_path)
    img_paths=utils.files.get_files(in_path,True)
    os.system("touch "+out_path)
    for img_i in img_paths:
        cmd="./features/extract_feats " + img_i +" "+out_path
        os.system(cmd)

def get_outpath(in_path,out_path):
    name=utils.files.get_name(in_path)
    name+=".txt"#name.replace(".jpg",".txt")
    return out_path+"/"+name

def unique_id_dec(in_path,out_path):
    print(in_path)
    dir_paths=utils.files.get_dirs(in_path,True)
    for k,dir_in_i in enumerate(dir_paths):
        dir_out_i=utils.files.replace_path(dir_in_i,out_path)
        print(dir_in_i)
        print(dir_out_i)
        unique_id(k,dir_in_i,dir_out_i)
        #utils.files.conversion(dir_i,out_path,unique_id,True) 

def unique_id(k,in_path,out_path):
    dir_paths=utils.files.get_dirs(in_path,True)
    #print(dir_paths)
    utils.files.make_dir(out_path)
    for i,dir_i in enumerate(dir_paths):
        new_dir_i=utils.files.replace_path(dir_i,out_path)
        utils.files.make_dir(new_dir_i)
        files_paths=utils.files.get_files(dir_i,True)
        #print(files_paths)
        #dir_name=utils.files.get_name(dir_name)
        #utils.make_dir(new_dir_i)
        for j,file_i in enumerate(files_paths):
            name="frame" + str(k)+"_"+str(i)+"_"+str(j)+".jpg"
            full_path=utils.files.replace_path(name,new_dir_i)
            print(full_path)   
        #    print(file_i)
        #    print(full_path)
            copyfile(file_i,full_path)