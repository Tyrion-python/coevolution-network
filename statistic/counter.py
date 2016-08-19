__author__ = 'Tyrion'

import random

import networkx as nx

import statistic.statistic as sc


class Counter(sc.Statistic):
    def __init__(self, data_loader):
        super(Counter, self).__init__(data_loader)

    def count_citation_degree_distribution(self):
        paper_in_papers = self.data_loader.paper_in_papers
        degrees = [0] * 20000
        max_degree = 0
        for index in range(1, self.max_paper_index):
            in_papers = paper_in_papers[index]
            try:
                degree = len(in_papers)
                if degree > max_degree:
                    max_degree = degree
                degrees[degree] += 1
            except TypeError:
                pass
        del degrees[max_degree + 1:]
        print(sum(degrees))
        return degrees

    def count_average_and_max_distance(self, graph, times=100000):
        sub_graph = max(nx.connected_component_subgraphs(graph), key=len)
        calculate_distance(sub_graph, times)

    def count_all_coauthor_citation_gap_year(self):
        all_coauthor_citation_gap_year = {}
        author_coauthor_years = self.data_loader.author_coauthor_years

        for author in range(1, self.max_author_index):
            if author_coauthor_years[author] is None:
                continue
            coauthor_years = author_coauthor_years[author]
            for coauthor in coauthor_years:
                if coauthor < author:
                    continue
                years = author_coauthor_years[author][coauthor]
                for year in years:
                    self.calculate_all_gap_year(all_coauthor_citation_gap_year, author, coauthor, year)
        return all_coauthor_citation_gap_year

    def calculate_all_gap_year(self, all_coauthor_citation_gap_year, author, coauthor, coauthor_year):
        # the efficiency can be better
        try:
            cite_years0 = self.data_loader.author_cited_author_years[author][coauthor]
        except (KeyError, TypeError):
            cite_years0 = set()
        try:
            cite_years1 = self.data_loader.author_cited_author_years[coauthor][author]
        except (KeyError, TypeError):
            cite_years1 = set()
        cite_years = cite_years0 | cite_years1
        for cite_year in cite_years:
            try:
                all_coauthor_citation_gap_year[cite_year - coauthor_year] += 1
            except KeyError:
                all_coauthor_citation_gap_year[cite_year - coauthor_year] = 1

    def count_year_paper_number(self):
        year_paper_number = {}
        for year in self.paper_year:
            try:
                year_paper_number[year] += 1
            except KeyError:
                year_paper_number[year] = 1
        return year_paper_number

    def count_author_start_year(self):
        author_start_year = [2016] * self.max_author_index
        for paper in range(1, self.max_paper_index):
            authors = self.paper_authors[paper]
            year = self.paper_year[paper]
            for author in authors:
                if author_start_year[author] > year:
                    author_start_year[author] = year

        return author_start_year

    def count_author_old_or_new(self):
        author_start_year = self.count_author_start_year()
        old_new_author_number = [0] * 2
        for paper in range(1, self.max_paper_index):
            authors = self.paper_authors[paper]
            year = self.data_loader.paper_year[paper]
            for author in authors:
                if author_start_year[author] == year:
                    old_new_author_number[1] += 1
                else:
                    old_new_author_number[0] += 1
        print('old author: {}    new_author: {}'.format(old_new_author_number[0], old_new_author_number[1]))

    def count_all_coauthor_gap_year(self):
        all_coauthor_gap_year = {}
        for author in range(1, self.max_author_index):
            if self.data_loader.author_coauthor_years[author] is None:
                continue
            coauthor_years = self.data_loader.author_coauthor_years[author]
            for coauthor in coauthor_years:
                years = coauthor_years[coauthor]
                for year in years:
                    calculate_coauthor_gap_year(year, years, all_coauthor_gap_year)
        print(sum(list(all_coauthor_gap_year.values())))
        print(all_coauthor_gap_year)
        return all_coauthor_gap_year


def calculate_distance(graph, times):
    total_length = 0
    longest_path = 0
    node_array = []
    size = graph.number_of_nodes()
    array = graph.nodes()
    for i in range(0, size):
        node_array.append(array[i])

    for i in range(1, times + 1):
        while True:
            source = random.randint(0, size - 1)
            target = random.randint(0, size - 1)
            break;

        length = nx.shortest_path_length(graph, node_array[source], node_array[target])
        total_length = total_length + length
        if length > longest_path:
            longest_path = length
        if i % 10000 == 0:
            print('the diameter is: {}'.format(longest_path))
            average_length = float(total_length) / i
            print('the average length is: {}'.format(average_length))

    print('finish')


def calculate_coauthor_gap_year(target_year, years, coauthor_gap_year):
    for year in years:
        gap_year = year - target_year
        if gap_year > 0:
            try:
                coauthor_gap_year[gap_year] += 1
            except KeyError:
                coauthor_gap_year[gap_year] = 1
