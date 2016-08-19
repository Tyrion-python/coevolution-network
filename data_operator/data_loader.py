__author__ = 'Tyrion'

import networkx as nx

import data_operator.file_handle as fh
import statistic.statistic_tools as st


class DataLoader(fh.FileHandle):
    # paper_author_file_address: paper author year
    # paper_year_file:paper year
    # paper_citation_file:paper out_paper, year
    # coauthor_file:author coauthor year
    # all number was separated by \t
    def __init__(self, file_addresses, tag=True, max_author_index_1=None, max_paper_index_1=None):
        super(DataLoader, self).__init__(file_addresses)
        self.max_paper_index = 0
        self.max_author_index = 0
        self.get_max_index()

        if max_author_index_1 is not None:
            self.max_author_index_1 = max_author_index_1
            self.max_paper_index_1 = max_paper_index_1
        else:
            self.max_author_index_1 = self.max_author_index
            self.max_paper_index_1 = self.max_paper_index
        self.paper_year = [2016] * self.max_paper_index_1
        self.paper_authors = [None] * self.max_paper_index_1
        self.paper_out_papers = [None] * self.max_paper_index_1
        self.paper_in_papers = None

        if tag:
            self.set_paper_year()
            self.set_paper_authors()
            self.set_paper_out_papers()
            # self.set_paper_in_papers()

        self.author_cited_author_years = None
        self.author_coauthor_years = None
        self.author_papers = None
        self.author_coauthors = None
        self.author_coauthor_papers = None

    def get_max_index(self):
        max_index_file = open(self.max_index_file_address, 'r')
        line = max_index_file.readline()
        values = line.split('\t')
        self.max_author_index, self.max_paper_index = int(values[0]), int(values[1])
        print(self.max_author_index, self.max_paper_index)

    def set_paper_year(self):
        paper_year_file = open(self.paper_year_file_address, 'r')
        line = paper_year_file.readline()
        while line:
            values = line.split('\t')
            paper = int(values[0])
            year = int(values[1])
            self.paper_year[paper] = year
            line = paper_year_file.readline()
        paper_year_file.close()
        print('set paper year done')

    def set_paper_authors(self):
        paper_author_file = open(self.paper_author_file_address, 'r')
        line = paper_author_file.readline()
        while line:
            values = line.split('\t')
            paper = int(values[0])
            author = int(values[1])
            try:
                self.paper_authors[paper].add(author)
            except AttributeError:
                self.paper_authors[paper] = {author}
            line = paper_author_file.readline()
        paper_author_file.close()
        print('set paper authors done')

    def set_paper_out_papers(self):
        paper_citation_file = open(self.paper_citation_file_address, 'r')
        line = paper_citation_file.readline()
        while line:
            values = line.split('\t')
            paper = int(values[0])
            out_paper = int(values[1])
            try:
                self.paper_out_papers[paper].add(out_paper)
            except AttributeError:
                self.paper_out_papers[paper] = {out_paper}
            line = paper_citation_file.readline()
        paper_citation_file.close()
        print('set paper out papers done')

    def set_paper_in_papers(self):
        self.paper_in_papers = [None] * self.max_paper_index_1
        paper_citation_file = open(self.paper_citation_file_address, 'r')
        line = paper_citation_file.readline()
        while line:
            values = line.split('\t')
            paper = int(values[0])
            out_paper = int(values[1])
            try:
                self.paper_in_papers[out_paper].add(paper)
            except AttributeError:
                self.paper_in_papers[out_paper] = {paper}
            line = paper_citation_file.readline()
        paper_citation_file.close()

    def load_graph_from_file(self, graph_name='citation'):
        if graph_name == 'citation':
            # graph = nx.DiGraph()
            graph = nx.Graph()
            graph_file = open(self.paper_citation_file_address, 'r')
        else:
            graph = nx.Graph()
            graph_file = open(self.coauthor_file_address, 'r')
        line = graph_file.readline()
        while line:
            values = line.split('\t')
            node0 = int(values[0])
            node1 = int(values[1])
            graph.add_edge(node0, node1)
            line = graph_file.readline()

        return graph

    def set_author_cited_author_years(self):
        self.author_cited_author_years = [None] * self.max_author_index_1
        for paper in range(1, self.max_paper_index):
            out_papers = self.paper_out_papers[paper]
            if out_papers is None:
                continue
            authors = self.paper_authors[paper]
            year = self.paper_year[paper]
            for out_paper in out_papers:
                cited_authors = self.paper_authors[out_paper]
                if len(authors & cited_authors) != 0:
                    continue
                for author in authors:
                    for cited_author in cited_authors:  ##error!!!!!!
                        st.update_array_dict_set(self.author_cited_author_years, author, cited_author, year)

        print('set paper cited author year done')

    def set_author_coauthor_years(self, repeat=False):
        self.author_coauthor_years = [None] * self.max_author_index_1
        coauthor_file = open(self.coauthor_file_address, 'r')
        line = coauthor_file.readline()
        while line:
            values = line.split('\t')
            author0 = int(values[0])
            author1 = int(values[1])
            if author0 > author1:
                author0, author1 = author1, author0
            year = int(values[2])
            st.update_array_dict_set(self.author_coauthor_years, author0, author1, year)
            if repeat:
                st.update_array_dict_set(self.author_coauthor_years, author1, author0, year)
            line = coauthor_file.readline()
        coauthor_file.close()
        print('set paper author coauthor done')

    def set_author_papers(self):
        self.author_papers = [None] * self.max_author_index_1
        paper_author_file = open(self.paper_author_file_address, 'r')
        line = paper_author_file.readline()
        while line:
            values = line.split('\t')
            author = int(values[1])
            paper = int(values[0])
            try:
                self.author_papers[author].add(paper)
            except AttributeError:
                self.author_papers[author] = {paper}
            line = paper_author_file.readline()
        paper_author_file.close()

    def set_author_coauthors(self):
        self.author_coauthors = [None] * self.max_author_index_1
        coauthor_file = open(self.coauthor_file_address, 'r')
        line = coauthor_file.readline()
        while line:
            values = line.split('\t')
            author0 = int(values[0])
            author1 = int(values[1])
            try:
                self.author_coauthors[author0].add(author1)
            except AttributeError:
                self.author_coauthors[author0] = {author1}
            try:
                self.author_coauthors[author1].add(author0)
            except AttributeError:
                self.author_coauthors[author1] = {author0}
            line = coauthor_file.readline()
        coauthor_file.close()

    def set_author_coauthor_papers(self):
        self.author_coauthor_papers = [None] * self.max_author_index_1
        coauthor_file = open(self.coauthor_file_address, 'r')
        line = coauthor_file.readline()
        while line:
            values = line.split('\t')
            author0 = int(values[0])
            author1 = int(values[1])
            self.update_author_coauthor_papers(author0, author1)
            self.update_author_coauthor_papers(author1, author0)
            line = coauthor_file.readline()
        coauthor_file.close()

    def update_author_coauthor_papers(self, author, coauthor):
        coauthor_papers = self.author_papers[coauthor]
        for coauthor_paper in coauthor_papers:
            if author not in self.paper_authors[coauthor_paper]:
                try:
                    self.author_coauthor_papers[author].add(coauthor_paper)
                except AttributeError:
                    self.author_coauthor_papers[author] = {coauthor_paper}
