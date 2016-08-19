__author__ = 'Tyrion'

from math import exp

import statistic.statistic_tools as st


class ExchangeData:
    def __init__(self, **key_args):
        self.this_year = key_args['start_year']
        self.year_paper_number = key_args['year_paper_number']

        data_loader = key_args['data_loader']
        self.data_saver = key_args['data_saver']

        self.paper_year = data_loader.paper_year  # done1
        self.paper_authors = data_loader.paper_authors  # done1
        self.paper_out_papers = data_loader.paper_out_papers

        self.author_papers = data_loader.author_papers  # done1
        self.author_cited_author_years = data_loader.author_cited_author_years  # done1
        self.author_coauthor_papers = data_loader.author_coauthor_papers  # done1
        self.author_coauthor_years = data_loader.author_coauthor_years  # done1
        self.author_coauthors = data_loader.author_coauthors  # done1

        self.begin_paper_index = data_loader.max_paper_index
        self.begin_author_index = data_loader.max_author_index

        self.old_max_paper_index = data_loader.max_paper_index  # done 1
        self.max_paper_index = data_loader.max_paper_index  # done1
        self.old_max_author_index = data_loader.max_author_index  # done1
        self.max_author_index = data_loader.max_author_index  # done1

        self.final_author = 2000000
        self.final_paper = 2000000
        self.coauthor_degrees = [1] * self.final_author  # done
        self.citation_degrees = [0] * self.final_paper  # done

        self.coauthor_para = [120, 0.3]
        self.citation_para = [30, 0.3]
        self.co_co_para = [3300, 0.3]

        self.set_coauthor_degrees()
        self.set_citation_degrees()

        self.para_result = {}

    def update_max_paper_index(self):
        self.this_year += 1
        self.max_paper_index += self.year_paper_number[self.this_year]

    def set_coauthor_degrees(self):
        for i in range(1, self.max_author_index):
            try:
                self.coauthor_degrees[i] = len(self.author_coauthors[i]) + 1
            except TypeError:
                pass

    def set_citation_degrees(self):
        for i in range(1, self.max_paper_index):
            out_papers = self.paper_out_papers[i]
            if out_papers is None:
                continue
            for out_paper in out_papers:
                self.citation_degrees[out_paper] += 1

    def get_coauthor_power(self):
        coauthor_power = [0]
        temp_total = 0
        for i in range(1, self.old_max_author_index):
            temp_total += self.coauthor_degrees[i]
            coauthor_power.append(temp_total)
        return coauthor_power

    def get_paper_power(self):
        paper_power = [0]
        temp_total = 0
        for i in range(1, self.old_max_paper_index):
            factor = 7 * exp((self.paper_year[i] - self.this_year) / 5)
            temp_total += factor + self.citation_degrees[i]
            paper_power.append(temp_total)
        return paper_power

    def calculate_local_coauthor_power(self, author):
        local_coauthor_power = {}
        self.calculate_citation_effect(author, local_coauthor_power)
        self.calculate_friend_effect(author, local_coauthor_power)
        if len(local_coauthor_power) == 0:
            return
        return local_coauthor_power

    def calculate_citation_effect(self, author, local_coauthor_power):
        cited_author_years = self.author_cited_author_years[author]
        if cited_author_years is None:
            return
        for cited_author in cited_author_years:
            power = self.calculate_aging_power(cited_author_years[cited_author], self.coauthor_para)
            local_coauthor_power[cited_author] = power

    def calculate_friend_effect(self, author, local_coauthor_power):
        coauthor_years = self.author_coauthor_years[author]
        if coauthor_years is None:
            return
        for coauthor in coauthor_years:
            power = self.calculate_aging_power(coauthor_years[coauthor], self.co_co_para)
            try:
                local_coauthor_power[coauthor] += power
            except KeyError:
                local_coauthor_power[coauthor] = power

    def calculate_aging_power(self, year_array, para):
        factor = 0
        for year in year_array:
            gap_year = year - self.this_year
            try:
                factor += self.para_result[(gap_year, para[1])]
            except KeyError:
                result = exp(gap_year * para[1])
                self.para_result[(gap_year, para[1])] = result
                factor += result
        power = factor * para[0]
        return power

    '''def calculate_aging_power(self, year_array, para):
        factor = 0
        for year in year_array:
            factor += exp((year - self.this_year) * para[1])
        power = factor * para[0]
        return power'''

    def calculate_local_paper_power(self, author):
        local_paper_power = {}
        coauthor_papers = self.author_coauthor_papers[author]
        if coauthor_papers is None:
            return
        for paper in coauthor_papers:
            local_paper_power[paper] = self.calculate_single_paper_power(author, paper)
        return local_paper_power

    def calculate_single_paper_power(self, author, paper):
        coauthor_years = self.author_coauthor_years[author]
        coauthors = self.paper_authors[paper]
        power_list = []
        for coauthor in coauthors:
            if coauthor in coauthor_years:
                power = self.calculate_aging_power(coauthor_years[coauthor], self.citation_para)
                power_list.append(power)
        return max(power_list)

    def update_data(self, paper_authors, paper_cited_papers):
        self.old_max_paper_index = self.max_paper_index
        self.old_max_author_index = self.max_author_index

        self.update_author_papers(paper_authors)
        self.update_author_coauthor_years(paper_authors)
        self.update_author_cited_author_years(paper_cited_papers)
        self.set_coauthor_degrees()
        self.coauthor_para[0] *= 1.2
        self.citation_para[0] *= 1.2
        self.co_co_para[0] *= 1.2

    def update_author_papers(self, paper_authors):
        for paper in paper_authors:
            self.paper_year[paper] = self.this_year
            authors = paper_authors[paper]
            for author in authors:
                try:
                    self.paper_authors[paper].add(author)
                except AttributeError:
                    self.paper_authors[paper] = {author}
                try:
                    self.author_papers[author].add(paper)
                except AttributeError:
                    self.author_papers[author] = {paper}

    def update_author_coauthor_years(self, paper_authors):
        for paper in paper_authors:
            authors = paper_authors[paper]
            length = len(authors)
            for i in range(0, length - 1):
                for j in range(i + 1, length):
                    try:
                        self.author_coauthors[authors[i]].add(authors[j])
                    except AttributeError:
                        self.author_coauthors[authors[i]] = {authors[j]}
                    try:
                        self.author_coauthors[authors[j]].add(authors[i])
                    except AttributeError:
                        self.author_coauthors[authors[j]] = {authors[i]}
                st.update_array_dict_set(self.author_coauthor_years, authors[i], authors[j], self.this_year)
                st.update_array_dict_set(self.author_coauthor_years, authors[j], authors[i], self.this_year)
                self.update_author_coauthor_papers(authors[i], authors[j])
                self.update_author_coauthor_papers(authors[j], authors[i])

    def update_author_cited_author_years(self, paper_cited_papers):
        for paper in paper_cited_papers:
            self.paper_out_papers[paper] = paper_cited_papers[paper]
            authors = self.paper_authors[paper]
            cited_papers = paper_cited_papers[paper]
            for cited_paper in cited_papers:
                self.citation_degrees[cited_paper] += 1
                cited_authors = self.paper_authors[cited_paper]
                if len(authors & cited_authors) != 0:
                    continue
                for author in authors:
                    for cited_author in cited_authors:
                        st.update_array_dict_set(self.author_cited_author_years, author, cited_author, self.this_year)

    def update_author_coauthor_papers(self, author, coauthor):
        try:
            coauthor_papers = self.author_papers[coauthor]
        except TypeError:
            print(coauthor)
        for coauthor_paper in coauthor_papers:
            if author not in self.paper_authors[coauthor_paper]:
                try:
                    self.author_coauthor_papers[author].add(coauthor_paper)
                except AttributeError:
                    self.author_coauthor_papers[author] = {coauthor_paper}

    def save_all_files(self):
        self.data_saver.open_all_files('a+')
        self.data_saver.save_all(self.paper_year, self.paper_authors, self.paper_out_papers, self.begin_paper_index,
                                 self.max_paper_index, self.max_author_index)
        self.data_saver.close_all_files()
