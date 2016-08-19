__author__ = 'Tyrion'

import random

import coevolution_model.model_tools as mt
import coevolution_model.scholar_model as sm


class CoauthorModel(sm.ScholarModel):
    def __init__(self, exchange_data, alpha=0.2):
        self.alpha = alpha
        super(CoauthorModel, self).__init__(exchange_data)

    def update_coauthor_network(self):
        paper_authors = {}
        coauthor_power = self.exchange_data.get_coauthor_power()
        for paper_index in range(self.exchange_data.old_max_paper_index, self.exchange_data.max_paper_index):
            authors = self.do_new_author_increase(coauthor_power)
            paper_authors[paper_index] = authors
        return paper_authors

    def do_new_author_increase(self, coauthor_power):

        random_number = random.random()
        if random_number < self.alpha:
            authors = self.do_alpha_increase()
        else:
            authors = self.do_opposite_alpha_increase(coauthor_power)
        return authors

    def do_alpha_increase(self):
        begin_author_index = self.exchange_data.max_author_index
        authors = [begin_author_index, begin_author_index + 1, begin_author_index + 2]
        self.exchange_data.max_author_index += 3
        return authors

    def do_opposite_alpha_increase(self, coauthor_power):
        new_author = self.exchange_data.max_author_index
        self.exchange_data.max_author_index += 1
        chose_author = mt.choose_key_proportional_to_value(coauthor_power)
        coauthor = self.choose_global_coauthor(chose_author, coauthor_power)
        return [chose_author, new_author, coauthor]

    def choose_global_coauthor(self, chose_author, coauthor_power):
        local_coauthor_power = self.exchange_data.calculate_local_coauthor_power(chose_author)
        coauthor = mt.choose_key_proportional_to_value(coauthor_power, local_coauthor_power)
        return coauthor
