import pickle
import os
import glob
import json

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
