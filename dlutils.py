def check_rectangle(rectangular_coordinates):
    '''
    Check if the input rectangle coordinates are legal
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
    :param area_intersection:the area where two rectangles intersect.
    :return:area_union:area of two rectangular phases
    '''
    au_check = check_rectangle(au)
    bu_check = check_rectangle(bu)
    if au_check == False or bu_check == False:
        raise ('Error:The coordinates of the upper left point are '
               'not less than the coordinates of the lower right point')
    area_a = (au[2] - au[0]) * (au[3] - au[1])
    area_b = (bu[2] - bu[0]) * (bu[3] - bu[1])
    area_union = area_a + area_b - area_intersection
    return area_union


def intersection(ai, bi):
    '''
    Find the area where two rectangles intersect.
    Horizontal x axis and vertical y axis.
    :param ai:(x1,y1,x2,y2):(x1,y1)is top_left_point,(x2,y2)is right_lower_point
    :param bi:Same as ai
    :return:area:the area where two rectangles intersect.
    '''
    ai_check = check_rectangle(ai)
    bi_check = check_rectangle(bi)
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
    Find the cross ratio of two rectangles.
    :param a:(x1,y1,x2,y2):(x1,y1)is top_left_point,(x2,y2)is right_lower_point.
    :param b:Same as a.
    :return:cross ratio of two rectangles.
    '''
    area_i = intersection(a, b)
    area_u = union(a, b, area_i)
    ratio = float(area_i) / float(area_u + 1e-6)
    return ratio
