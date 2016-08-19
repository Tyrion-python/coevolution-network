__author__ = 'Tyrion'


class FileHandle:
    def __init__(self, file_addresses):
        self.paper_author_file_address = file_addresses['paper_author']
        self.paper_year_file_address = file_addresses['paper_year']
        self.paper_citation_file_address = file_addresses['paper_citation']
        self.coauthor_file_address = file_addresses['coauthor']
        self.max_index_file_address = file_addresses['max_index']
