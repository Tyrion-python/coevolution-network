__author__ = 'Tyrion'

import random


def choose_key_proportional_to_value(container, temp_container=None):
    if type(container) == dict:
        total_values = sum(list(container.values()))
        threshold = random.uniform(0, total_values)
        temp_total = 0
        for key in container:
            temp_total += container[key]
            if temp_total >= threshold:
                return key
    elif type(container) == list and temp_container is None:
        threshold = random.uniform(0, container[-1])
        return binary_search(container, threshold)
    elif type(container) == list and temp_container is not None:
        return additional_binary_search(container, 1, temp_container)


def binary_search(array, value, start=1):
    if value < array[0] or value > array[-1]:
        print('not in this array')
        return
    end = len(array) - 1
    while True:
        middle = int((start + end) / 2)
        if value <= array[middle]:
            if value > array[middle - 1]:
                return middle
            else:
                end = middle - 1
        else:
            start = middle + 1


def additional_binary_search(array, start=1, temp_container=None):
    temp_dict = {}
    index = len(array)
    short_end = index
    temp_total = array[-1]
    for key in temp_container:
        temp_total += temp_container[key]
        array.append(temp_total)
        temp_dict[index] = key
        index += 1

    threshold = random.uniform(0, array[-1])
    position = binary_search(array, threshold)
    if position >= short_end:
        position = temp_dict[position]

    end = len(array)
    for i in range(short_end, end):
        del array[-1]
    return position


def choose_key_add_key(array, container, temp_container=None):
    if container is None:
        return
    chose_key = choose_key_proportional_to_value(container, temp_container)
    if chose_key not in array:
        array.append(chose_key)
