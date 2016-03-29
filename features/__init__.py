import utils 
import utils.files
import os

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