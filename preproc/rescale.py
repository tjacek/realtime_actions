import cv2
#import utils.files as files

DIM_X=60
DIM_Y=60

def rescale(in_path,out_path):
    img=cv2.imread(in_path,cv2.IMREAD_GRAYSCALE)
    img=bounding_box(img)
    res = cv2.resize(img,(DIM_X,DIM_Y), interpolation = cv2.INTER_CUBIC)
    cv2.imwrite(out_path,res)

def bounding_box(img):
    ret,thresh = cv2.threshold(img,1,255,cv2.THRESH_BINARY)
    contours = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnt=contours[0]
    x_0,y_0,w,h=cv2.boundingRect(img)
    x_w=x_0+h
    y_h=y_0+w
    return img[x_0:x_w, y_0:y_h]

if __name__ == "__main__":
    rescale("preproc/out.jpg","preproc/rescaled.jpg")