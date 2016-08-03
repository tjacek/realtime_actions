import sys,os
sys.path.append(os.path.abspath('../realtime_actions'))
from xml.dom import minidom 
import cv2
import numpy as np
import utils.dirs

def read_xml_img(path):
    DOMTree = minidom.parse(path)
    cNodes = DOMTree.childNodes
    return cNodes[0]

@utils.dirs.ApplyToDirs()
def convert_img(in_path,out_path):
    in_path=str(in_path)
    out_path=str(out_path)
    xml=read_xml_img(str(in_path))
    width=parse_int(xml,"width")
    height=parse_int(xml,"height")
    raw_matrix=read_matrix(xml)
    raw_matrix=preproc_matrix(raw_matrix)
    if(len(raw_matrix)==width*height):
        mat = np.zeros((width,height), dtype=np.float32)
        y_i=0
        x_i=0
        for i,n_i in enumerate(raw_matrix):
            mat[x_i][y_i]=n_i
            x_i+=1
            if(x_i==width):
                x_i=0
                y_i+=1	
        mat=mat.T
        out_path=out_path.replace(".xml",".jpg")
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
    numbers=[float(n_i) for n_i in numbers
                   if n_i!='']
    return numbers

def preproc_matrix(matrix):
    min_val=min(matrix)
    max_val=max(matrix)
    matrix=[m_i -min_val+1.0 for m_i in matrix]
    matrix=[ (m_i/max_val +0.1)*255.0 for m_i in matrix]
    return matrix

if __name__ == "__main__":
    in_path='../dataset5/depth'
    out_path='../dataset5/raw'
    convert_img(in_path,out_path)