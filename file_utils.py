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

def load_plk(load_path):
    '''
    Load python variables
    :param load_path: load path
    :return:python variables
    '''
    with open(load_path, 'rb') as plk_f:
        plk = pickle.load(plk_f)
    return plk
