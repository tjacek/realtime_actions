import sys,os
sys.path.append(os.path.abspath('../realtime_actions'))
import utils.dirs

@utils.dirs.apply_to_files
def remove_planes(in_path,out_path):
    cmd="./ransac/remove_planes "+str(in_path)+" "+str(out_path)
    os.system(cmd)

if __name__ == "__main__":
    in_path='../dataset7/raw'
    out_path='../dataset7/ransac'
    remove_planes(in_path,out_path)