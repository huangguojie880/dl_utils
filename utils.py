import sys

def schedule(operationcount,totaloperations):
    '''
    可以显示当前的操作进度的百分比
    :param operationcount: 当前的操作已经的操作数
    :param totaloperations: 总共的操作数
    :return: 
    '''
    if round(operationcount * 100 / totaloperations) != round((operationcount + 1) * 100 / totaloperations):
        print('\r|', end='')
        print('#' * round((operationcount + 1) * 100 / totaloperations / 2), end='')
        print(' ' * (50 - round((operationcount + 1) * 100 / totaloperations / 2)), end='')
        print('|  ' + str(round((operationcount + 1) * 100 / totaloperations)) + '%', end='')
        sys.stdout.flush()
