import cv2
import utils.files as files

DIM_X=60
DIM_Y=60

def rescale(in_path,out_path):
    in_paths=files.get_files(in_path,True)
    for in_path_i in in_paths:
        img=cv2.imread(in_path_i)
        res = cv2.resize(img,(DIM_X,DIM_Y), interpolation = cv2.INTER_CUBIC)
        dst_path=files.replace_path(in_path_i,out_path)
        cv2.imwrite(dst_path,res)		