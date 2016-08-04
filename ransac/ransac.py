import sys,os
sys.path.append(os.path.abspath('../realtime_actions'))
import utils.dirs

@utils.dirs.ApplyToDirs()
def remove_planes(in_path,out_path):
    cmd="./ransac/remove_planes "+str(in_path)+" "+str(out_path)
    os.system(cmd)

if __name__ == "__main__":
    in_path='../dataset5/raw'
    out_path='../dataset5/ransac'
    remove_planes(in_path,out_path)