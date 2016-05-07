import numpy as np
import cv2
import paths
from dirs import dir_arg,file_dec, ApplyToFiles

class Image(np.ndarray):
    def __new__(cls,name,input_array,org_dim=None):
        if(org_dim==None):
            if(type(input_array)==Image):
                org_dim=input_array.org_dim
            else:
                org_dim=[input_array.shape[0],input_array.shape[1]]
        input_array=input_array.astype(float) 
        input_array=input_array.flatten()
        obj = np.asarray(input_array).view(cls) 
        obj.name=name
        obj.org_dim=org_dim
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return
        self.name = getattr(obj,'name', None)
        self.org_dim = getattr(obj,'org_dim', None)

    def get_orginal(self):
        img_i=self.astype(np.uint8)
        return np.reshape(img_i,self.org_dim)

    def flat2D(self):
        return self.reshape((1,self.shape[0]))

def img_dec(func):
    def inner_func(in_path,out_path):
        img=read_raw(in_path)
        new_img=func(img)
        cv2.imwrite(out_path,new_img)
    return inner_func

@file_dec
def read_images(file_path):
    img_i=read_raw(file_path)
    if(img_i!=None):
        return Image(file_path.get_name(),img_i)
    return None

def read_raw(img_path):
    return cv2.imread(str(img_path),cv2.IMREAD_GRAYSCALE) 

@paths.path_args
def save_img(out_path,img):
    img=img.get_orginal()
    #img*=250.0
    img=img.astype(np.uint8)
    full_path=out_path.copy().append(img.name)
    cv2.imwrite(str(full_path),img)

@ApplyToFiles(True)
@ApplyToFiles(False)
def rescale(in_path,out_path,new_dim=(60,120)):    
    img=cv2.imread(str(in_path))
    if(img!=None):
        new_img=cv2.resize(img,new_dim)
        cv2.imwrite(str(out_path),new_img)

if __name__ == "__main__":
    path="../../dataset9/"
    rescale(path+"actions",path+"final")
    #print(len(imgs))
    #unify_dirs(data,"test2")