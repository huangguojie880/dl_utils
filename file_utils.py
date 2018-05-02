import pickle

def save_plk(plk, save_path):
    '''
    Save python variables
    :param plk:Need to save python variables
    :param save_path: save path
    :return: None
    '''
    with open(save_path, 'wb') as config_f:
        pickle.dump(plk, config_f)
