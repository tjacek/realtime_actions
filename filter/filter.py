import sys,os
sys.path.append(os.path.abspath('../realtime_actions'))
import utils.dirs

@utils.dirs.ApplyToDirs()
def segment(in_path,out_path):
    cmd="./filter/remove_outliers "+str(in_path)+" "+str(out_path)
    os.system(cmd)

if __name__ == "__main__":
    in_path='../dataset5/ransac'
    out_path='../dataset5/segment'
    segment(in_path,out_path)