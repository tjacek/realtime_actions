from xml.dom import minidom 

DOMTree = minidom.parse('depth.xml')

cNodes = DOMTree.childNodes
img_xml=cNodes[0].getElementsByTagName("opencv_storage")

print img_xml.toxml()