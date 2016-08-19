__author__ = 'Tyrion'

import data_operator.file_handle as fh
import statistic.statistic_tools as st


class DataSaver(fh.FileHandle):
    def __init__(self, file_addresses):
        super(DataSaver, self).__init__(file_addresses)

        self.paper_citation_file = None
        self.paper_year_file = None
        self.paper_author_file = None
        self.coauthor_file = None
        self.max_index_file = None

    def open_file(self, file_tag, mode='r'):
        if file_tag == 'paper_author':
            self.paper_author_file = open(self.paper_author_file_address, mode)
        elif file_tag == 'paper_year':
            self.paper_year_file = open(self.paper_year_file_address, mode)
        elif file_tag == 'paper_citation':
            self.paper_citation_file = open(self.paper_citation_file_address, mode)
        elif file_tag == 'coauthor':
            self.coauthor_file = open(self.coauthor_file_address, mode)
        elif file_tag == 'max_index':
            self.max_index_file = open(self.max_index_file, mode)

    def close_file(self, file_tag):
        if file_tag == 'paper_author':
            self.paper_author_file.close()
        elif file_tag == 'paper_year':
            self.paper_year_file.close()
        elif file_tag == 'paper_citation':
            self.paper_citation_file.close()
        elif file_tag == 'coauthor':
            self.coauthor_file.close()
        elif file_tag == 'max_index':
            self.max_index_file.close()

    def open_all_files(self, mode):
        self.paper_citation_file = open(self.paper_citation_file_address, mode)
        self.paper_year_file = open(self.paper_year_file_address, mode)
        self.paper_author_file = open(self.paper_author_file_address, mode)
        self.coauthor_file = open(self.coauthor_file_address, mode)
        self.max_index_file = open(self.max_index_file_address, mode)

    def close_all_files(self):
        self.paper_citation_file.close()
        self.paper_year_file.close()
        self.paper_author_file.close()
        self.coauthor_file.close()
        self.max_index_file.close()

    def update_paper_year_file(self, paper, year):
        output_str = str(paper) + '\t' + str(year) + '\n'
        self.paper_year_file.write(output_str)

    def update_paper_author_file(self, paper, author, year):
        output_str = str(paper) + '\t' + str(author) + '\t' + str(year) + '\n'
        self.paper_author_file.write(output_str)

    def update_paper_citation_file(self, paper, cited_papers, year):
        for cited_paper in cited_papers:
            output_str = str(paper) + '\t' + str(cited_paper) + '\t' + str(year) + '\n'
            self.paper_citation_file.write(output_str)

    def update_coauthor_file(self, author0, author1, year):
        output_str = str(author0) + '\t' + str(author1) + '\t' + str(year) + '\n'
        self.coauthor_file.write(output_str)

    def update_max_index_file(self, max_author_index, max_paper_index):
        self.max_index_file.close()
        self.max_index_file = open(self.max_index_file_address,'w')
        output_str = str(max_author_index) + '\t' + str(max_paper_index) + '\n'
        self.max_index_file.write(output_str)

    def save_paper_authors(self, paper_year, paper_authors, begin_index, end_index):
        for paper in range(begin_index, end_index):
            authors = paper_authors[paper]
            for author in authors:
                year = paper_year[paper]
                self.update_paper_author_file(paper, author, year)

    def save_paper_year(self, paper_year, begin_index, end_index):
        for paper in range(begin_index, end_index):
            self.update_paper_year_file(paper, paper_year[paper])

    def save_paper_citation(self, paper_year, paper_cited_papers, begin_index, end_index):
        for paper in range(begin_index, end_index):
            cited_papers = paper_cited_papers[paper]
            self.update_paper_citation_file(paper, cited_papers, paper_year[paper])

    def save_coauthor(self, paper_year, paper_authors, begin_index, end_index):
        for paper in range(begin_index, end_index):
            year = paper_year[paper]
            authors = list(paper_authors[paper])
            length = len(authors)
            for i in range(0, length - 1):
                for j in range(i + 1, length):
                    self.update_coauthor_file(authors[i], authors[j], year)

    def save_all(self, paper_year, paper_authors, paper_out_papers, begin_index, end_index, max_author_index):
        self.save_paper_year(paper_year, begin_index, end_index)
        self.save_paper_authors(paper_year, paper_authors, begin_index, end_index)
        self.save_paper_citation(paper_year, paper_out_papers, begin_index, end_index)
        self.save_coauthor(paper_year, paper_authors, begin_index, end_index)
        self.update_max_index_file(max_author_index, end_index)