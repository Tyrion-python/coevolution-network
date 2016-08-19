__author__ = 'Tyrion'

__author__ = 'Tyrion'

import data_operator.data_saver as ds
import data_operator.file_handle as fh


class IndexFormatter(fh.FileHandle):
    def __init__(self, file_addresses, file_addresses_end_year, end_year):
        super(IndexFormatter, self).__init__(file_addresses)
        self.data_saver = ds.DataSaver(file_addresses_end_year)
        self.file_addresses_end_year = file_addresses_end_year
        self.citation_index_map = {}
        self.coauthor_index_map = {}
        self.max_paper_index = 1
        self.max_author_index = 1
        self.end_year = end_year

    def format(self):
        self.data_saver.open_all_files('w')
        self.format_paper_year_index()
        self.format_paper_citation_index()
        self.format_paper_author_file()
        self.format_coauthor_file()
        self.data_saver.update_max_index_file(self.max_author_index, self.max_paper_index)
        self.data_saver.close_all_files()

    def format_paper_author_file(self):
        paper_author_file = open(self.paper_author_file_address, 'r')
        line = paper_author_file.readline()
        while line:
            values = line.split('\t')
            paper_str = values[0]
            if paper_str in self.citation_index_map:
                (index, self.max_author_index) = update_index_map(self.coauthor_index_map, self.max_author_index,
                                                                  values[1])
                self.data_saver.update_paper_author_file(self.citation_index_map[paper_str], index, int(values[2]))
            line = paper_author_file.readline()
        paper_author_file.close()

    def format_paper_year_index(self):
        paper_year_file = open(self.paper_year_file_address, 'r')
        line = paper_year_file.readline()
        while line:
            values = line.split('\t')
            year = int(values[1])
            if year <= self.end_year:
                index, self.max_paper_index = update_index_map(self.citation_index_map, self.max_paper_index, values[0])
                self.data_saver.update_paper_year_file(index, year)
            line = paper_year_file.readline()
        paper_year_file.close()

    def format_paper_citation_index(self):
        citation_file = open(self.paper_citation_file_address, 'r')
        line = citation_file.readline()
        while line:
            values = line.split('\t')
            year = int(values[2])
            if year <= self.end_year:
                node0 = self.citation_index_map[values[0]]
                try:
                    node1 = self.citation_index_map[values[1]]
                    self.data_saver.update_paper_citation_file(node0, [node1], year)
                except KeyError:
                    print(line)
            line = citation_file.readline()
        citation_file.close()

    def format_coauthor_file(self):
        coauthor_file = open(self.coauthor_file_address, 'r')
        line = coauthor_file.readline()
        while line:
            values = line.split('\t')
            year = int(values[2])
            if year <= self.end_year:
                self.data_saver.update_coauthor_file(self.coauthor_index_map[values[0]],
                                                     self.coauthor_index_map[values[1]], year)
            line = coauthor_file.readline()
        coauthor_file.close()


def update_index_map(index_map, max_index, node):
    if node in index_map:
        index = index_map[node]
    else:
        index = max_index
        index_map[node] = max_index
        max_index += 1
    return index, max_index
