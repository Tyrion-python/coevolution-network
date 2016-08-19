__author__ = 'Tyrion'

import time

import coevolution_model.exchange_data as ed
import coevolution_model.coauthor_model as crl
import coevolution_model.citation_model as cnl


class UnitedModel:
    def __init__(self, **key_args):
        exchange_data = ed.ExchangeData(**key_args)
        self.exchange_data = exchange_data
        self.coauthor_model = crl.CoauthorModel(exchange_data, key_args['alpha'])
        self.citation_model = cnl.CitationModel(exchange_data)

    def go_end_year(self, end_year):
        start_time = time.time()
        while self.exchange_data.this_year < end_year:
            self.exchange_data.update_max_paper_index()
            paper_authors = self.coauthor_model.update_coauthor_network()
            paper_cited_papers = self.citation_model.update_citation_network(paper_authors)
            print(self.exchange_data.old_max_paper_index, self.exchange_data.max_paper_index)
            self.exchange_data.update_data(paper_authors, paper_cited_papers)
            end_time = time.time()
            print(end_time - start_time)

    def save_files(self):
        self.exchange_data.save_all_files()