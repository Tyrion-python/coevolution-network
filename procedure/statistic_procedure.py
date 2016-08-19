__author__ = 'Tyrion'

import networkx as nx
import pylab as pl

import data_operator.file_tools as ft
import procedure.statistic_data_preparation as sdp
import plot.plot as pt
import statistic.counter as cr
import statistic.filter as fr
import statistic.statistic_tools as st

if 'filter' in sdp.running_modes[sdp.index]:
    paper_filter = fr.PaperFilter(sdp.data_loader)
elif 'count' in sdp.running_modes[sdp.index]:
    counter = cr.Counter(sdp.data_loader)

if sdp.index == 0:
    paper_filter.filter_valid_papers()
if sdp.index == 1:
    degrees = counter.count_citation_degree_distribution()
    ft.save_data_to_file(degrees, 'list array citation in degree distribution.txt')
    x, y = pt.get_xy_from_container(degrees)
    y = st.div_sum_array(y)
    folder = sdp.file_address_container.get_file_addresses(sdp.source_folder, 'plot')
    pt.plot_figure(pl.loglog, x, y, 'list citation_number_distribution', folder, 'citation number(log10)', 'percent(log10)')
if sdp.index == 2:
    degrees = nx.degree_histogram(sdp.coauthor_graph)
    ft.save_data_to_file(degrees, 'list coauthor degree distribution.txt')
    x, y = st.get_xy_from_container(degrees)
    y = st.div_sum_container(y)
    folder = sdp.file_address_container.get_file_addresses(sdp.source_folder, 'plot')
    pt.plot_figure(pl.loglog, x, y, 'coauthor_number_distribution', folder, 'citation number(log10)', 'percent(log10)')
if sdp.index == 3:
    largest_cc = max(nx.connected_components(sdp.citation_graph), key=len)
    print(len(largest_cc))
if sdp.index == 4:
    largest_cc = max(nx.connected_components(sdp.coauthor_graph), key=len)
    print(len(largest_cc))
if sdp.index == 5:
    print(nx.average_clustering(sdp.coauthor_graph))
if sdp.index == 6:
    counter.count_average_and_max_distance(sdp.coauthor_graph)
if sdp.index == 7:
    all_gap_year = counter.count_all_coauthor_citation_gap_year()
    citation_count, coauthor_count = st.count_frequency(all_gap_year, 0)
    ft.save_data_to_file(all_gap_year, 'dict all coauthor citation gap year.txt')
    all_gap_year[0] = 1
    st.div_sum_container(all_gap_year, 0, citation_count, coauthor_count)
    x, y = st.get_xy_from_container(all_gap_year)
    y = st.log_10_array(y)
    folder = sdp.file_address_container.get_file_addresses(sdp.source_folder, 'plot')
    pt.plot_figure(pl.plot, x, y, 'all coauthor citation gap year', folder, 'gap year', 'percent(log10)')
if sdp.index == 8:
    year_paper_number = counter.count_year_paper_number()
    ft.save_data_to_file(year_paper_number, 'year paper number.txt')
if sdp.index == 9:
    counter.count_author_old_or_new()
if sdp.index == 10:
    print(len(sdp.coauthor_graph.edges()))
if sdp.index == 11:
    all_coauthor_gap_year = counter.count_all_coauthor_gap_year()
    ft.save_data_to_file(all_coauthor_gap_year, 'dict all coauthor gap year.txt')
    x, y = st.get_xy_from_container(all_coauthor_gap_year)
    y[0] = 0
    y = st.div_sum_container(y)
    y = st.log_10_array(y)
    folder = sdp.file_address_container.get_file_addresses(sdp.source_folder, 'plot')
    pt.plot_figure(pl.plot, x, y, 'all coauthor gap year', folder, 'gap year', 'percent(log10)')
