__author__ = 'Tyrion'

import shutil


def cut_file_by_end_year(original_file_address, new_file_address, year_col, end_year):
    original_file = open(original_file_address, 'r')
    new_file = open(new_file_address, 'w')
    line = original_file.readline()
    while line:
        values = line.split('\t')
        if int(values[year_col]) <= end_year:
            new_file.write(line)
        line = original_file.readline()
    original_file.close()
    new_file.close()


def save_data_to_file(container, file_address='dictionary.txt'):
    file_handler = open(file_address, 'w')
    if type(container) == set:
        for value in container:
            file_handler.write(str(value) + '\n')
    elif type(container) == list:
        length = len(container)
        for index in range(0, length):
            file_handler.write(str(index) + '\t' + str(container[index]) + '\n')
    elif type(container) == dict:
        for key in container:
            file_handler.write(str(key) + '\t' + str(container[key]) + '\n')
    file_handler.close()


def load_data_to_file(saved_file_address):
    saved_file = open(saved_file_address, 'r')
    if 'dict' in saved_file_address:
        container = {}
        line = saved_file.readline()
        while line:
            values = line.split('\t')
            container[int(values[0])] = int(values[1])
            line = saved_file.readline()
    elif 'set' in saved_file_address:
        container = set()
        line = saved_file.readline()
        while line:
            container.add(int(line))
            line = saved_file.readline()
    saved_file.close()
    return container


def cut_file_by_tag(tags, original_file_address, new_file_address, cols):
    original_file = open(original_file_address, 'r')
    new_file = open(new_file_address, 'w')
    line = original_file.readline()
    while line:
        values = line.split('\t')
        flag = True
        for col in cols:
            tag = int(values[col])
            if tag in tags:
                flag = False
                break
        if flag:
            new_file.write(line)
        line = original_file.readline()
    original_file.close()
    new_file.close()


def write_coauthor_file(paper_authors, paper_year, file_address):
    file = open(file_address, 'w')
    for index in range(1, len(paper_authors)):
        authors = paper_authors[index]
        if authors is None:
            continue
        year = paper_year[index]
        length = len(authors)
        authors_array = list(authors)
        for i in range(0, length - 1):
            for j in range(i + 1, length):
                string = (str(authors_array[i]), str(authors_array[j]), str(year))
                file.write('\t'.join(string) + '\n')


def copy_file(src, dst):
    shutil.copy(src, dst)


def copy_backup_file(file_folder_address):
    file_folder_name = file_folder_address[:-1]
    try:
        shutil.rmtree(file_folder_name)
    except FileNotFoundError:
        pass
    backup_file_folder_name = file_folder_name + '_backup'
    shutil.copytree(backup_file_folder_name, file_folder_name)
