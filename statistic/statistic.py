__author__ = 'Tyrion'


class Statistic:
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.paper_out_papers = data_loader.paper_out_papers
        # self.paper_in_papers = data_loader.paper_in_papers
        self.paper_authors = data_loader.paper_authors
        self.paper_year = data_loader.paper_year
        self.max_author_index = data_loader.max_author_index
        self.max_paper_index = data_loader.max_paper_index



