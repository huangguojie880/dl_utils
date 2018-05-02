import xml.etree.ElementTree as ET

def check_box(rectangular_coordinates):
    '''
    Check if the input box coordinates are legal
    :param Rectangular_coordinates:(x1,y1,x2,y2) where x1,y1 are the coordinates of the top-left point,
    and x2,y2 are the coordinates of the bottom-right point
    :return: False is illegal,True is legal
    '''
    x1 = rectangular_coordinates[0]
    y1 = rectangular_coordinates[1]
    x2 = rectangular_coordinates[0]
    y2 = rectangular_coordinates[1]
    if x1 >= x2 or y1 >= y2:
        return False
    else:
        return True

def union(au, bu, area_intersection):
    '''
    Find the area of two rectangular phases
    :param au:(x1,y1,x2,y2):(x1,y1)is top_left_point,(x2,y2)is right_lower_point
    :param bu:same as au
    :param area_intersection:the area where two boxes intersect.
    :return:area_union:area of two rectangular phases
    '''
    au_check = check_box(au)
    bu_check = check_box(bu)
    if au_check == False or bu_check == False:
        raise ('Error:The coordinates of the upper left point are '
               'not less than the coordinates of the lower right point')
    area_a = (au[2] - au[0]) * (au[3] - au[1])
    area_b = (bu[2] - bu[0]) * (bu[3] - bu[1])
    area_union = area_a + area_b - area_intersection
    return area_union


def intersection(ai, bi):
    '''
    Find the area where two boxes intersect.
    Horizontal x axis and vertical y axis.
    :param ai:(x1,y1,x2,y2):(x1,y1)is top_left_point,(x2,y2)is right_lower_point
    :param bi:Same as ai
    :return:area:the area where two boxes intersect.
    '''
    ai_check = check_box(ai)
    bi_check = check_box(bi)
    if ai_check == False or bi_check == False:
        raise ('Error:The coordinates of the upper left point are '
               'not less than the coordinates of the lower right point')
    x = max(ai[0], bi[0])
    y = max(ai[1], bi[1])
    w = min(ai[2], bi[2]) - x
    h = min(ai[3], bi[3]) - y
    if w < 0 or h < 0:
        return 0
    area = w * h
    return area


def iou(a, b):
    '''
    Find the cross ratio of two boxes.
    :param a:(x1,y1,x2,y2):(x1,y1)is top_left_point,(x2,y2)is right_lower_point.
    :param b:Same as a.
    :return:cross ratio of two boxes.
    '''
    area_i = intersection(a, b)
    area_u = union(a, b, area_i)
    ratio = float(area_i) / float(area_u + 1e-6)
    return ratio

def all_boxes(annot_path):
    '''
    The xml format is the same as pascal_voc.
    Get all boxes under the xml file.
    :param annot_path: Xml path
    :return boxes:all boxes under the xml file.
    '''
    et = ET.parse(annot_path)
    element = et.getroot()
    element_objs = element.findall('object')
    boxes = []
    for element_obj in element_objs:
        obj_bbox = element_obj.find('bndbox')
        x1 = int(round(float(obj_bbox.find('xmin').text)))
        y1 = int(round(float(obj_bbox.find('ymin').text)))
        x2 = int(round(float(obj_bbox.find('xmax').text)))
        y2 = int(round(float(obj_bbox.find('ymax').text)))
        boxes.append([x1,y1,x2,y2])
    return boxes

def max_iou(box,all_boxes):
    '''
    The maximum ratio of a given box to target boxes.
    The box format is:(x1,y1,x2,y2)
    :param box:given box
    :param all_boxes:target boxes
    :return:iou_num_max:maximum ratio
              iou_num_max_box:Corresponding box
    '''
    iou_num_max = 0
    iou_num_max_box = [0, 0, 0, 0]
    for one_box in all_boxes:
        iou_num = iou(box,one_box)
        if iou_num>iou_num_max:
            iou_num_max = iou_num
            iou_num_max_box[0] = one_box[0]
            iou_num_max_box[1] = one_box[1]
            iou_num_max_box[2] = one_box[2]
            iou_num_max_box[3] = one_box[3]
    return iou_num_max,iou_num_max_box
