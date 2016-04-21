import dirs
import files
import shutil

def select_data(in_path,out_path,prefix="bin"):
    dirs.make_dir(out_path)
    all_files=dirs.get_files(in_path)
    prefix_files=[f for f in all_files 
	                if files.extract_prefix(str(f))==prefix]
    out_files=[out_path.create(path_i.get_name()) 
                  for path_i in prefix_files]
    for in_file,out_file in zip(in_prefix_files,out_prefix_files):
        shutil.copyfile(in_file, out_file)
        print(in_file)
    
if __name__ == "__main__":
    path="../dataset2/"
    in_path=path+"MSRDailyAct3D_pack1/"
    out_path=path+"binary"
    select_data(in_path,out_path)