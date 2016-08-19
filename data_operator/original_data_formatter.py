__author__ = 'Tyrion'


class OriginalDataFormatter:
    _FILE_Folder = 'data_set/original_data/'
    _PAPER_AUTHOR_FILE = 'col_authorid_paperid_authorpos.txt'
    _PAPER_YEAR_FILE = 'paper_year_nouse.txt'
    _PAPER_CITATION_FILE = 'paper_cited_paper_year.txt'

    def __init__(self, data_saver, max_author_index=1712434, max_paper_index=2092357):
        self._max_author_index = max_author_index
        self._max_paper_index = max_paper_index
        self._paper_year = [2016] * max_paper_index
        self.data_saver = data_saver

    def format_paper_year_file(self):
        local_file_handle = open(self._FILE_Folder + self._PAPER_YEAR_FILE, 'r')
        line = local_file_handle.readline()
        count = 0
        while line:
            values = line.split('\t')
            paper = int(values[0])
            try:
                year = int(values[1])
            except ValueError:
                year = 2016
            self._paper_year[paper] = year
            self.data_saver.update_paper_year_file(paper, year)
            line = local_file_handle.readline()
        local_file_handle.close()

    def format_paper_author_file(self):
        paper_author_file = open(self._FILE_Folder + self._PAPER_AUTHOR_FILE)
        line = paper_author_file.readline()
        while line:
            values = line.split('\t')
            author = int(values[1])
            paper = int(values[2])
            self.data_saver.update_paper_author_file(paper, author, self._paper_year[paper])
            line = paper_author_file.readline()
        paper_author_file.close()

    def set_paper_cited_papers(self):
        paper_citation_file = open(self.paper_citation_file_address, 'r')
        line = paper_citation_file.readline()
        while line:
            values = line.split('\t')
            paper = int(values[0])
            cited_paper = int(values[1])
            if paper in self.paper_cited_papers:
                self.paper_cited_papers[paper].append(cited_paper)
            else:
                self.paper_cited_papers[paper] = [cited_paper]
            line = paper_citation_file.readline()
        paper_citation_file.close()