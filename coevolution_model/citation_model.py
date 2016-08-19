__author__ = 'Tyrion'

import coevolution_model.model_tools as mt
import coevolution_model.scholar_model as sm


class CitationModel(sm.ScholarModel):
    def __init__(self, exchange_data):
        super(CitationModel, self).__init__(exchange_data)

    def update_citation_network(self, paper_authors):
        old_max_author_index = self.exchange_data.old_max_author_index
        paper_power = self.exchange_data.get_paper_power()
        paper_cited_papers = {}
        for paper in paper_authors:
            key_author = paper_authors[paper][0]
            cited_papers = []
            local_paper_power = None
            for i in range(0, 4):
                if key_author >= old_max_author_index:
                    mt.choose_key_add_key(cited_papers, paper_power)
                else:
                    if local_paper_power is None:
                        local_paper_power = self.exchange_data.calculate_local_paper_power(key_author)
                    mt.choose_key_add_key(cited_papers, paper_power, local_paper_power)
            paper_cited_papers[paper] = cited_papers
        return paper_cited_papers
