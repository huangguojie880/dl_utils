import xml.etree.ElementTree as ET
from keras.utils import to_categorical
import os
from PIL import Image
import numpy as np

import pickle

def save_plk(plk, save_path):
    '''
    Save python variables
    :param plk:Need to save python variables
    :param save_path: save path
    :return: None
    '''
    with open(save_path, 'wb') as plk_f:
        pickle.dump(plk, plk_f)

def check_box(box_coordinates):
    '''
    Check if the input box coordinates are legal
    :param Rectangular_coordinates:(x1,y1,x2,y2) where x1,y1 are the coordinates of the top-left point,
    and x2,y2 are the coordinates of the bottom-right point
    :return: False is illegal,True is legal
    '''
    x1 = box_coordinates[0]
    y1 = box_coordinates[1]
    x2 = box_coordinates[2]
    y2 = box_coordinates[3]
    if x1 > x2 or y1 > y2:
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
        raise ('Error:The coordinates of the upper left point are not less than the coordinates of the lower right point')
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
        raise ('Error:The coordinates of the upper left point are not less than the coordinates of the lower right point')
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
        flag = check_box([x1,y1,x2,y2])
        if flag == False:
            raise ('Error:The coordinates of the upper left point are not less than the coordinates of the lower right point')
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

def get_box(img):
    '''
    二值图像，得到包含物体的框
    :param img:
    :return:
    '''
    x = []
    y = []
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i,j] != 0:
                x.append(j)
                y.append(i)
    x1 = min(x)
    x2 = max(x)
    y1 = min(y)
    y2 = max(y)
    return [x1,y1,x2,y2]

def get_pointBox(img,img_box,box):
    '''
    得到每一个点对应的box
    :param img: 二值图片
    :param img_box: 存储点属性的数组
    :param box: 所有点属于哪个box
    :return:
    '''
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i,j] != 0:
                img_box[i, j, 0] = box[0]
                img_box[i, j, 1] = box[1]
                img_box[i, j, 2] = box[2]
                img_box[i, j, 3] = box[3]
    return img_box

def get_plk(path,save_path):
    '''
    :param path: objectseg所在的路径
    :param save_path:保存plk的路径:
    :return: None
    '''

    for name in os.listdir(path):
        file = os.path.join(path,name)
        img = Image.open(file)
        label  = img.convert('P')
        label = np.array(label)
        label[label == 255] = 0
        label = to_categorical(label)
        img_box =  np.zeros(shape=(label.shape[0],label.shape[1],4))
        for i in range(1,label.shape[2]):
            temp = label[:,:,i]
            box = get_box(temp)
            img_box = get_pointBox(temp,img_box,box)
        one_save_path = save_path + '/' + name.split('.')[0] + '.plk'
        save_plk(img_box,one_save_path)
        
def get_regr_data(point,box):
    '''
    :param point: 中心点在原图上对应的坐标（x,y）
    :param box: 中心点属于哪一个框(x1,y1,x2,y2),框的中心点：cx = 0.5*(x1+x2),cy = 0.5*(y1+y2)
    :return: 中心点的回归梯度(a1,a2,b1,b2)
    a1,a2是中心点位置回归
    a1 = （x - cx）/slen
    a2 = (y - cy) /slen
    b1,b2是边框长度回归
    b1 = (|x - cx| + blen)/(x2 - x1)
    b2 = (|y - cy| + blen)/(y2 - y1)
    '''
    x = point[0]
    y = point[1]
    x1 = box[0]
    y1 = box[1]
    x2 = box[2]
    y2 = box[3]
    cx = (x1 + x2)/2
    cy = (y1 + y2)/2
    a1 = (x - cx)/slen
    a2 = (y - cy) /slen
    b1 = (np.abs(x - cx) + blen)/(x2 - x1)
    b2 = (np.abs(y - cy) + blen)/(y2 - y1)
    return (a1,a2,b1,b2)
