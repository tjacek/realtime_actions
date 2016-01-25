from xml.dom import minidom 
import cv2
import numpy as np

def read_xml_img(path):
    DOMTree = minidom.parse(path)
    cNodes = DOMTree.childNodes
    return cNodes[0]

def read_img(in_path,out_path):
    xml=read_xml_img(in_path)
    width=parse_int(xml,"width")
    height=parse_int(xml,"height")
    raw_matrix=read_matrix(xml)
    if(len(raw_matrix)==width*height):
        mat = np.zeros((width,height), dtype=np.uint8)
        y_i=0
        x_i=0
        for i,n_i in enumerate(raw_matrix):
            mat[x_i][y_i]=n_i
            x_i+=1
            if(x_i==width):
                x_i=0
                y_i+=1	
        #img=cv2.cvtColor(mat, cv2.COLOR_BGR2GRAY)
        mat=mat.T
        cv2.imwrite(out_path,mat)

def parse_int(node,name):
    raw=node.getElementsByTagName(name)[0]
    raw=raw.firstChild.data
    return int(raw)

def read_matrix(node):
    raw=node.getElementsByTagName("data")[0]
    raw=raw.firstChild.data
    raw=raw.replace("\n","")
    numbers=raw.split(" ")
    numbers=[int(n_i) for n_i in numbers
                   if n_i!='']
    return numbers

read_img("depth.xml","out.jpg") #img_xml.nodeType == img_xml.ELEMENT_NODE