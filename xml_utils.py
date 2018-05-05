import xml.dom.minidom

def create_xml(filename,img_width,img_height,boxes,save_path):
    doc = xml.dom.minidom.Document()
    root = doc.createElement('annotation')
    doc.appendChild(root)

    nodeSize = doc.createElement('size')
    nodeWidth = doc.createElement('width')
    nodeWidth.appendChild(doc.createTextNode(str(img_width)))
    nodeHeight = doc.createElement('height')
    nodeHeight.appendChild(doc.createTextNode(str(img_height)))
    nodeSize.appendChild(nodeWidth)
    nodeSize.appendChild(nodeHeight)
    nodeFilename = doc.createElement('filename')
    nodeFilename.appendChild(doc.createTextNode(filename))

    root.appendChild(nodeFilename)
    root.appendChild(nodeSize)


    for box in boxes:
        nodeObject = doc.createElement('object')
        nodeName = doc.createElement('name')
        nodeName.appendChild(doc.createTextNode('car'))
        nodeDifficult = doc.createElement('difficult')
        nodeDifficult.appendChild(doc.createTextNode('0'))

        nodeBndbox = doc.createElement('bndbox')
        nodeXmin = doc.createElement('xmin')
        nodeXmin.appendChild(doc.createTextNode(str(box['xmin'])))
        nodeYmin = doc.createElement('ymin')
        nodeYmin.appendChild(doc.createTextNode(str(box['ymin'])))
        nodeXmax = doc.createElement('xmax')
        nodeXmax.appendChild(doc.createTextNode(str(box['xmax'])))
        nodeYmax = doc.createElement('ymax')
        nodeYmax.appendChild(doc.createTextNode(str(box['ymax'])))
        nodeBndbox.appendChild(nodeXmin)
        nodeBndbox.appendChild(nodeYmin)
        nodeBndbox.appendChild(nodeXmax)
        nodeBndbox.appendChild(nodeYmax)
        nodeObject.appendChild(nodeDifficult)
        nodeObject.appendChild(nodeName)
        nodeObject.appendChild(nodeBndbox)
        root.appendChild(nodeObject)

    #开始写xml文档
    fp = open(save_path, 'w')
    doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")
