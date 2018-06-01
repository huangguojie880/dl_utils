import pickle
import os
import glob

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
