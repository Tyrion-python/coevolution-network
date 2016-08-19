__author__ = 'Tyrion'

import pylab as pl
import data_operator.data_loader as dl
import data_operator.file_address_container as fac
import data_operator.file_tools as ft
import data_operator.data_saver as ds
import coevolution_model.united_model as um
import statistic.counter as cr
import statistic.statistic_tools as st
import plot.plot as pt

source_folder = 'model'
start_year = 1960
end_year = 1962

file_address_container = fac.FileAddressContainer()
ft.copy_backup_file(file_address_container.get_file_addresses(source_folder, 'scholar', True))

year_paper_number = ft.load_data_to_file('dict year paper number.txt')
data_loader = dl.DataLoader(file_address_container.get_file_addresses(source_folder), True, 2000000, 20000000)
data_loader.set_author_papers()
data_loader.set_author_coauthors()
data_loader.set_author_cited_author_years()
data_loader.set_author_coauthor_years(repeat=True)
data_loader.set_author_coauthor_papers()

data_saver = ds.DataSaver(file_address_container.get_file_addresses(source_folder))

united_model = um.UnitedModel(alpha=0.1, year_paper_number=year_paper_number, start_year=start_year,
                              data_loader=data_loader, data_saver=data_saver)
united_model.go_end_year(end_year)

data_loader.max_author_index = united_model.exchange_data.max_author_index
counter = cr.Counter(data_loader)
all_gap_year = counter.count_all_coauthor_citation_gap_year()
citation_count, coauthor_count = st.count_frequency(all_gap_year,0)
print('citation_count {} coauthor_count {}'.format(citation_count, coauthor_count))
all_gap_year[0] = 1
st.div_sum_container(all_gap_year, 0, citation_count, coauthor_count)

x, y = st.get_xy_from_container(all_gap_year)
y = st.log_10_array(y)
folder = file_address_container.get_file_addresses(source_folder, 'plot')
pt.plot_figure(pl.plot, x, y, 'all coauthor citation gap year', folder, 'gap year', 'percent(log10)')
