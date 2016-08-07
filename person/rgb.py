import cv2

def clean(grey_path,rgb_path,out_path):
    grey_img = cv2.imread(grey_path)
    rgb_img= cv2.imread(rgb_path)
    rgb_img=cv2.resize(rgb_img, (0,0), fx=0.5, fy=0.5)
    print(grey_img.shape)
    print(rgb_img.shape)
    rgb_img[grey_img==0]=0
    cv2.imwrite(out_path,rgb_img)

clean('grey.jpg','rgb.jpg','in.jpg')