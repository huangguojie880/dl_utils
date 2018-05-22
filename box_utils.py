import xml.etree.ElementTree as ET
from keras.utils import to_categorical
import os
from PIL import Image
import numpy as np
import simplecv2 as sv2
import pickle
from collections import Counter

def save_plk(plk, save_path):
    '''
    Save python variables
    :param plk:Need to save python variables
    :param save_path: save path
    :return: None
    '''
    with open(save_path, 'wb') as plk_f:
        pickle.dump(plk, plk_f)
        
def load_plk(load_path):
    '''
    Load python variables
    :param load_path: load path
    :return:python variables
    '''
    with open(load_path, 'rb') as plk_f:
        plk = pickle.load(plk_f)
    return plk


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
        raise (
        'Error:The coordinates of the upper left point are not less than the coordinates of the lower right point')
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
        raise (
        'Error:The coordinates of the upper left point are not less than the coordinates of the lower right point')
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
        flag = check_box([x1, y1, x2, y2])
        if flag == False:
            raise (
            'Error:The coordinates of the upper left point are not less than the coordinates of the lower right point')
        boxes.append([x1, y1, x2, y2])
    return boxes


def max_iou(box, all_boxes):
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
        iou_num = iou(box, one_box)
        if iou_num > iou_num_max:
            iou_num_max = iou_num
            iou_num_max_box[0] = one_box[0]
            iou_num_max_box[1] = one_box[1]
            iou_num_max_box[2] = one_box[2]
            iou_num_max_box[3] = one_box[3]
    return iou_num_max, iou_num_max_box


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
            if img[i, j] != 0:
                x.append(j)
                y.append(i)
    x1 = min(x)
    x2 = max(x)
    y1 = min(y)
    y2 = max(y)
    return [x1, y1, x2, y2]


def get_pointBox(img, img_box, box):
    '''
    得到每一个点对应的box
    :param img: 二值图片
    :param img_box: 存储点属性的数组
    :param box: 所有点属于哪个box
    :return:
    '''
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i, j] != 0:
                img_box[i, j, 0] = box[0]
                img_box[i, j, 1] = box[1]
                img_box[i, j, 2] = box[2]
                img_box[i, j, 3] = box[3]
    return img_box


def get_pointBoxPlk(path, save_path):
    '''
    得到包含改点的box属性
    :param path: objectseg所在的路径
    :param save_path:保存plk的路径:
    :return: None
    '''

    for name in os.listdir(path):
        file = os.path.join(path, name)
        img = Image.open(file)
        label = img.convert('P')
        label = np.array(label)
        label[label == 255] = 0
        label = to_categorical(label)
        img_box = np.zeros(shape=(label.shape[0], label.shape[1], 4))
        for i in range(1, label.shape[2]):
            temp = label[:, :, i]
            box = get_box(temp)
            img_box = get_pointBox(temp, img_box, box)
        one_save_path = save_path + '/' + name.split('.')[0] + '.plk'
        save_plk(img_box, one_save_path)


def get_regr_data(point, box,slenI=64):
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
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    a1 = (x - cx) / slenI
    a2 = (y - cy) / slenI
    b1 = (np.abs(x - cx) + slenI) / (x2 - x1)
    b2 = (np.abs(y - cy) + slenI) / (y2 - y1)
    return (a1, a2, b1, b2)


def get_sumPoint(img):
    '''
    得到该图像内非0像素点的个数
    :param img:
    :return:
    '''
    img_shape = img.shape
    num = 0
    for i in range(int(img_shape[0])):
        for j in range(int(img_shape[1])):
            if img[i, j] != 0:
                num += 1
    return num


def getRate_array(img, slenI=64):
    '''
    将img切成边长为slenI的小方块，得到每一个小方块中非0值占的比例的array
    :param img:
    :param slenI:
    :return: shape为[int(img_shape[0]/slenI),int(img_shape[1]/slenI)]
    '''
    img_shape = img.shape
    outData_row = int(img_shape[0] / slenI)
    outData_col = int(img_shape[1] / slenI)
    out_data = np.zeros(shape=(outData_row, outData_col))
    for i in range(outData_row):
        for j in range(outData_col):
            temp = img[i * slenI:(i + 1) * slenI, j * slenI:(j + 1) * slenI]
            num = get_sumPoint(temp)
            rate = num / (slenI * slenI)
            out_data[i, j] = rate
    return out_data


def get_trainPointClassPlk(path, save_path, ilenI=512, slenI=64, classesI=21):
    '''
    将img切成边长为slenI的小方块，得到每一个小方块属于哪一类
    :param path: classseg所在的路径
    :param save_path:保存plk的路径:
    return: shape为[ilenI/slenI,ilenI/slenI,classesI]
    '''

    for name in os.listdir(path):
        print(name)
        file = os.path.join(path, name)
        img = Image.open(file)
        label = img.convert('P')
        label = np.array(label)
        label[label == 255] = 0
        label = to_categorical(label, classesI)
        label = sv2.resize_image_with_crop_or_pad(label, (ilenI, ilenI))
        label_shape = label.shape
        outData_row = int(label_shape[0] / slenI)
        outData_col = int(label_shape[1] / slenI)
        img_rateArray = np.zeros(shape=(outData_row, outData_col, classesI))
        for i in range(1, label.shape[2]):
            temp = label[:, :, i]
            img_rateArray[:, :, i] = getRate_array(temp, slenI)
        img_class = np.argmax(img_rateArray, axis=-1)
        img_class = to_categorical(img_class, classesI)
        one_save_path = save_path + '/' + name.split('.')[0] + '.plk'
        save_plk(img_class, one_save_path)
        
def box2name(box):
    '''
    将box变成字符串类型，每一个坐标以"_'隔开
    :param box:
    :return:
    '''
    return str(box[0])+'_'+str(box[1])+'_'+str(box[2])+'_'+str(box[3])

def name2box(name):
    '''
    将字符串类型的box，变为int类型的box
    :param name:
    :return:
    '''
    x1 = int(float(name.split('_')[0]))
    y1 = int(float(name.split('_')[1]))
    x2 = int(float(name.split('_')[2]))
    y2 = int(float(name.split('_')[3]))
    return [x1,y1,x2,y2]


def get_maxNumBox(img_pointBox):
    '''
    得到img_pointBox里，最多的box坐标
    :param img_pointBox:
    :return:
    '''
    img_shape = img_pointBox.shape
    boxes = []
    for i in range(int(img_shape[0])):
        for j in range(int(img_shape[1])):
            if sum(img_pointBox[i, j,:]) != 0:
                boxes.append(box2name(img_pointBox[i, j,:]))
    if len(boxes) != 0:
        boxes_count = Counter(boxes)
        box = boxes_count.most_common(1)[0][0]
        box = name2box(box)
    else:
        box = [0,0,0,0]
    return box


def get_imgBoxRegrPlk(path, save_path, ilenI = 512, slenI = 64):
    '''
    将img切成边长为slenI的小方块，得到每一个小方块属于的regr
    :param path: classsegBox所在的路径
    :param save_path:保存plk的路径:
    return: shape为[ilenI/slenI,ilenI/slenI,classesI]
    '''
    
    for name in os.listdir(path):
        print(name)
        file = os.path.join(path, name)
        img_pointBox = load_plk(file)
        img_pointBox = sv2.resize_image_with_crop_or_pad(img_pointBox, (ilenI, ilenI))
        outData_row = int(ilenI / slenI)
        outData_col = int(ilenI/ slenI)
        img_trainDataRegr = np.zeros(shape=(outData_row, outData_col, 4))
        for i in range(outData_row):
            for j in range(outData_col):
                temp = img_pointBox[i * slenI:(i + 1) * slenI, j * slenI:(j + 1) * slenI,:]
                box = get_maxNumBox(temp)
                
                ci = i * 64 + 32
                cj = j * 64 + 32
                if sum(box) != 0:
                    regr = get_regr_data((ci,cj), box, slenI)
                else:
                    regr = [0,0,0,0]
                img_trainDataRegr[i,j,:] = regr
        one_save_path = save_path + '/' + name.split('.')[0] + '.plk'
        save_plk(img_trainDataRegr, one_save_path)
