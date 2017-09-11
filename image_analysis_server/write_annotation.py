#Written by Shitao Tang
# --------------------------------------------------------
import xml.dom.minidom as xdm
import os,logging
from xml.dom.minidom import Document

def xml_node(doc,name,text):
    node=doc.createElement(name)
    node.appendChild(doc.createTextNode(text))
    return node

def generate_bounding_boxes_xml(doc,object_name,xmin,ymin,xmax,ymax,score):
    """Create an object node"""
    object_node=doc.createElement('object')

    #object name
    name_node=doc.createElement('name')
    name_node.appendChild(doc.createTextNode(object_name))
    object_node.appendChild(name_node)

    object_node.appendChild(xml_node(doc,'score',str(score)))

    #bounding box
    bnd_node=doc.createElement('bndbox')
    bnd_node.appendChild(xml_node(doc,'xmin',str(int(xmin))))
    bnd_node.appendChild(xml_node(doc,'ymin',str(int(ymin))))
    bnd_node.appendChild(xml_node(doc,'xmax',str(int(xmax))))
    bnd_node.appendChild(xml_node(doc,'ymax',str(int(ymax))))
    object_node.appendChild(bnd_node)

    return object_node


def generate_image_xml(image_name,size,bounding_box):
    """Generate xml result for image according to bounding box"""
    logging.info("begin generating xml file")
    path='annotation'
    import re
    #cut off the suffix
    pattern=re.compile('.+\.')
    xml_name=os.path.join(path,pattern.search(image_name).group()[0:-1]+'.xml')

    doc=Document()

    #create root
    annotation=doc.createElement('annotation')

    #create image name node
    annotation.appendChild(xml_node(doc,'filename',image_name))

    #create size node
    size_node=doc.createElement('size')
    size_node.appendChild(xml_node(doc,'width',str(size[0])))
    size_node.appendChild(xml_node(doc,'height',str(size[1])))
    size_node.appendChild(xml_node(doc,'depth',str(size[2])))
    annotation.appendChild(size_node)

    #create object node
    for name,boxes in bounding_box.items():
        for box in boxes:
            annotation.appendChild(generate_bounding_boxes_xml(doc,name,box[0],box[1],box[2],box[3],box[4]))
    doc.appendChild(annotation)

    logging.info("finish generating xml file")
    return doc.toprettyxml(indent=' ')
