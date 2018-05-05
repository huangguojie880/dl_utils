import keras.backend as K
import tensorflow as tf

'''
Introduce:Show training status
Examole:
from keras.utils import generic_utils
progbar = generic_utils.Progbar(epoch_num)
progbar.update(step_num,[('name1', value1)), ('name2', value2)])
'''

def focal_mse(r = 1):
    '''
    A focal mse loss function
    :param r: The coefficient is several times
    :return: -
    '''
    def mse(y_true, y_pred):
        return K.mean((tf.abs(y_true - y_pred)**r)*tf.losses.sigmoid_cross_entropy( y_pred,y_true))
