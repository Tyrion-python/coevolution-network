__author__ = 'Tyrion'

__author__ = 'Tyrion'

import data_operator.file_tools as ft
import statistic.statistic as sc


class PaperFilter(sc.Statistic):
    def __init__(self, data_loader):
        super(PaperFilter, self).__init__(data_loader)

    def filter_valid_papers(self, end_year=2012):
        invalid_papers = set()
        self.except_wrong_citation_papers(invalid_papers)
        print(len(invalid_papers))
        self.except_end_year_paper(invalid_papers, end_year)
        print(len(invalid_papers))
        self.except_no_author_paper(invalid_papers)
        print(len(invalid_papers))
        ft.save_data_to_file(invalid_papers, 'invalid_papers_set.txt')
        # self.remove_edges_of_invalid_papers(invalid_papers)
        # self.except_no_citation_papers()

    def except_wrong_citation_papers(self, invalid_papers):
        for paper in range(1, self.max_paper_index):
            if self.paper_out_papers[paper] is not None:
                out_papers = self.paper_out_papers[paper]
                for out_paper in out_papers:
                    if self.paper_year[out_paper] > self.paper_year[paper]:
                        invalid_papers.add(paper)

    def except_end_year_paper(self, invalid_papers, end_year):
        for paper in range(1, self.max_paper_index):
            if self.paper_year[paper] > end_year:
                invalid_papers.add(paper)

    def except_no_author_paper(self, invalid_papers):
        for paper in range(1, self.max_paper_index):
            if self.paper_authors[paper] is None:
                invalid_papers.add(paper)

    def except_no_citation_papers(self):
        invalid_papers = set()
        for paper in range(1, self.max_paper_index):
            if self.paper_out_papers[paper] is None:
                invalid_papers.add(paper)
        print(len(invalid_papers))

    def remove_edges_of_invalid_papers(self, invalid_papers):
        for invalid_paper in invalid_papers:
            self.remove_in_edges(invalid_paper)
            self.remove_out_edges(invalid_paper)
            self.paper_in_papers[invalid_paper] = None
            self.paper_out_papers[invalid_paper] = None

    def remove_in_edges(self, invalid_paper):
        in_papers = self.paper_in_papers[invalid_paper]
        if in_papers is not None:
            for in_paper in in_papers:
                self.paper_out_papers[in_paper].remove(invalid_paper)
                if len(self.paper_out_papers[in_paper]) == 0:
                    self.paper_out_papers[in_paper] = None

    def remove_out_edges(self, invalid_paper):
        out_papers = self.paper_out_papers[invalid_paper]
        if out_papers is not None:
            for out_paper in out_papers:
                self.paper_in_papers[out_paper].remove(invalid_paper)
                if len(self.paper_in_papers[out_paper]) == 0:
                    self.paper_in_papers[out_paper] = None
