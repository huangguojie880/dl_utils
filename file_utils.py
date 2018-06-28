import pickle
import os
import glob
import json

def load_file_list(path=None, printable=True):
    r"""
    Parameters
    ----------
    path : str or None
        A folder path, if `None`, use the current directory.
    printable : boolean
        Whether to print the files infomation.
    Examples
    ----------
    """
    if path is None:
        path = os.getcwd()
    file_list = os.listdir(path)
    file_list.sort()
    if printable:
        print('Match file list = %s' % file_list)
        print('Number of files = %d' % len(file_list))
    return file_list

def read_images(img_list, path='', printable=True):
    """Returns all images in list by given path and name of each image file.
    Parameters
    -------------
    img_list : list of str
        The image file names.
    path : str
        The image folder path.
    printable : boolean
        Whether to print information when reading images.
    Returns
    -------
    list of numpy.array
        The images.
    """
    imgs = []
    for img_name in img_list:
        img_path = os.path.join(path,img_name)
        img = load_img(img_path)
        img = img_to_array(img)
        imgs.append(img)
    if printable == True:
        print('read %d from %s' % (len(imgs), path))
    return imgs


def exists_or_mkdir(path, verbose=True):
    """Check a folder by given name, if not exist, create the folder and return False,
    if directory exists, return True.
    Parameters
    ----------
    path : str
        A folder path.
    verbose : boolean
        If True (default), prints results.
    Returns
    --------
    boolean
        True if folder already exist, otherwise, returns False and create the folder.
    Examples
    --------
    >>> tl.files.exists_or_mkdir("checkpoints/train")
    """
    if not os.path.exists(path):
        if verbose:
            print("[*] creates %s ..." % path)
        os.makedirs(path)
        return False
    else:
        if verbose:
            print("[!] %s exists ..." % path)
        return True

def save_plk(save_thing,save_path):
    '''
    Save python variables
    :param save_thing:Need to save python variables
    :param save_path: save path
    :return: 如果保存出错则返回错误原因，否则无返回值
    '''
    try:
        with open(save_path, 'wb') as plk_f:
            pickle.dump(save_thing, plk_f)
        return None
    except Exception as e:
        return e

def load_plk(load_path):
    '''
    Load python variables
    :param load_path: load path
    :return:python variables,出错则返回错误原因
    '''
    try:
        with open(load_path, 'rb') as plk_f:
            plk = pickle.load(plk_f)
        return plk
    except Exception as e:
        return e

def get_filesList(generalTerm):
    '''
    得到一个路径下某一后缀名的所有文件路径
    :param generalTerm: 列如'ground-truth/*.txt'
    :return: 所有文件路径的list
    '''
    files_list = glob.glob(generalTerm)
    return files_list

def get_currentDir():
    '''
    得到当前文件夹的路径
    :return:
    '''
    current_dir = os.path.dirname(os.path.realpath(__file__))
    return current_dir

def path_check(path):
    '''
    检查路径是否存在，不存在即创建文件夹。
    它会把该路径下缺的文件夹都创建，但不可以创建文件
    :param path:
    :return: 存在该路径为True，不存在返回False
    '''
    path_list = path.split('/')
    path_temp = path_list[0]
    flag = None
    for i in range(1,len(path_list)):
        path_temp += '/' + path_list[i]
        flag = os.path.exists(path_temp)
        if flag is False:
            os.mkdir(path_temp)
    return flag

def file_lines_to_list(path):
    '''
    将文件里的每一行作为一条数据存储在list中
    :param path:
    :return:
    '''
    with open(path) as f:
        content = f.readlines()
        # remove whitespace characters like `\n` at the end of each line
        content = [x.strip() for x in content]
    return content

def save_json(save_thing,save_path):
    '''
    将python对象保存为json文件
    :param save_thing: 保存的python对象
    :param save_path: 保存路径
    :return: 如果保存出错则返回错误原因，否则无返回值
    '''
    try:
        with open(save_path, 'w') as outfile:
            json.dump(save_thing, outfile)
            return None
    except Exception as e:
        return e
