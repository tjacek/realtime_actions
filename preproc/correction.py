import utils.files as files
import cv2

def correct_actions(in_path,out_path):
    action,frame_names=read_action(in_path)
    correction(action)	
    save_action(action,frame_names)

def read_action(path):
    frame_names=files.get_files(path,append=True)
    frames=[cv2.imread(frame_name_i,cv2.IMREAD_GRAYSCALE) for frame_name_i in frame_names]
    return frames,frame_names

def save_action(action,frame_names):
    for i,path_i in enumerate(frame_names):
        cv2.imwrite(path_i,action[i])

def correction(action):
    width=action[0].shape[0]
    height=action[0].shape[1]
    time=len(action)
    for i in range(width):
    	print(i)
        for j in range(height):
            for t in range(1,time-1):
                last=action[t-1][i][j]
                current=action[t][i][j]
                next=action[t+1][i][j]
                if(last==0 and next==0 and current!=0):
                    action[t][i][j]=0
                if(last!=0 and next!=0 and current==0):
                    action[t][i][j]=(last + next)/2.0
