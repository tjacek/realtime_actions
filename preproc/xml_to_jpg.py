from xml.dom import minidom 

DOMTree = minidom.parse('depth.xml')

print DOMTree.toxml()