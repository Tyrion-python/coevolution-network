__author__ = 'Tyrion'

import os


class FileAddressContainer:
    SCHOLAR_DATA_FOLDER = 'scholar_data/'
    PICTURES_FOLDER = 'pictures/'
    PLOT_PICTURES_FOLDER = 'plot_pictures/'
    DATA_SET_FOLDER = 'data_set/'
    # PAPER_AUTHOR_FILE = 'paper_author.txt'
    # PAPER_YEAR_FILE = 'paper_year.txt'
    # PAPER_CITATION_FILE = 'paper_citation.txt'
    # COAUTHOR_FILE = 'coauthor.txt'
    # CITATION_FILE = 'citation.txt'
    # TEMP_COAUTHOR_FILE = 'temp_coauthor.txt'

    YEAR_PAPER_NUMBER_FILE_NAME = 'year_paper_number.txt'
    scholar_file_tag = {'paper_author', 'paper_year', 'paper_citation', 'coauthor', 'max_index'}
    fold_tag = {'scholar': SCHOLAR_DATA_FOLDER, 'plot': PLOT_PICTURES_FOLDER}

    def get_file_addresses(self, out_folder, in_folder='scholar',folder=False):
        file_addresses = {}
        base_folder = self.DATA_SET_FOLDER + out_folder
        if not os.path.exists(base_folder):
            create_folder(base_folder)

        file_folder = self.DATA_SET_FOLDER + out_folder + '/' + self.fold_tag[in_folder]
        if not os.path.exists(file_folder):
            create_folder(file_folder)
        if folder:
            return file_folder

        if in_folder == 'scholar':
            for tag in self.scholar_file_tag:
                file_addresses[tag] = file_folder + tag + '.txt'
            print(file_addresses)
            return file_addresses
        elif in_folder == 'plot':
            print(file_folder)
            return file_folder

def create_folder(folder):
    os.makedirs(folder)
