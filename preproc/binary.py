import struct
import numpy as np 
import utils.dirs
import cv2

class Header(object):
   def __init__(self,n_frames,width,height):
       self.n_frames=n_frames
       self.width=width
       self.height=height
       self.frame_size=self.width*self.height

   def size(self):
       return self.n_frames*self.width*self.height
   
   def __str__(self):
       f=str(self.n_frames)
       w=str(self.width)
       h=str(self.height)
       return f +","+w+","+h +"\n"

class RawAction(object):
    def __init__(self,frames):
        self.frames=frames

@utils.dirs.ApplyToFiles()
def from_binary(action_path,out_path):
    raw_action=read_binary(str(action_path))
    action_name=action_path.get_name()
    action_name=action_name.split(".")[0]
    utils.dirs.make_dir(out_path)
    for i,frame_i in enumerate(raw_action.frames):     
        frame_i=standarize(frame_i)
        name=action_name+str(i)+".jpg"
        full_path=out_path.create(name)
        cv2.imwrite(str(full_path),frame_i)

def standarize(img):
    img_nonzero=np.nonzero(img)
    z_max=np.min(img[img_nonzero])-1
    img[img_nonzero]-=z_max
    return img

def read_binary(action_path):
    with open(action_path, mode='rb') as f:
    	int_action=np.fromfile(f, dtype=np.uint32)
    header=read_header(int_action)
    #print(header)
    assert (len(int_action)-header.size())==3
    frames=read_frames(header,int_action)
    return RawAction(frames)

def read_header(int_action):
    n_frames=int_action[0]
    width=int_action[1]
    height=int_action[2]
    return Header(n_frames,width,height)

def read_frames(hd,int_action):
    indexes=range(hd.n_frames)
    return [read_frame(i,int_action,hd) for i in indexes]

def read_frame(i,int_action,hd):
    start=3+i*hd.frame_size
    end=start+hd.frame_size
    frame=int_action[start:end]
    frame=np.array(frame)
    frame=frame.astype(float,copy=False)
    frame=np.reshape(frame,(hd.height,hd.width))
    return frame

if __name__ == "__main__":
    from_binary("preproc/action.bin","preproc/not_raw")