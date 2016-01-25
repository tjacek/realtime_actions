from xml.dom import minidom 
import cv2

def read_xml_img(path):
    DOMTree = minidom.parse(path)
    cNodes = DOMTree.childNodes
    return cNodes[0]

def read_img(path):
    xml=read_xml_img(path)
    width=parse_int(xml,"width")
    height=parse_int(xml,"height")
    raw_matrix=read_matrix(xml)
    if(len(raw_matrix)==width*height):
        print("OK")

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

read_img("depth.xml") #img_xml.nodeType == img_xml.ELEMENT_NODE