__author__ = 'Tyrion'

import math


def div_sum_container(container, *other_arg):
    if type(container) == list:
        total = sum(container)
        return [(z + 1) / total for z in container]
    if type(container) == dict and len(other_arg) != 0:
        for key in container:
            if key < other_arg[0]:
                container[key] /= other_arg[1]
            else:
                container[key] /= other_arg[2]


def get_xy_from_container(container):
    x = []
    y = []
    if type(container) == list:
        length = len(container)
        for i in range(0, length):
            x.append(i)
            y.append(container[i])
    elif type(container) == dict:
        for key in container:
            x.append(key)
            y.append(container[key])
    return x, y


def log_10_array(array):
    return [math.log10(z) for z in array]


def update_array_dict_set(array, index0, index1, value):
    try:
        array[index0][index1].add(value)
    except TypeError:
        array[index0] = {index1: {value}}
    except KeyError:
        array[index0][index1] = {value}


def count_frequency(container, split=None):
    if type(container) == dict and split is not None:
        count0 = 0
        count1 = 0
    for key in container:
        if key > split:
            count1 += container[key]
        elif key < 0:
            count0 += container[key]
    return count0,count1
