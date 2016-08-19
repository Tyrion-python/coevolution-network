__author__ = 'Tyrion'

import pylab as pl

import data_operator.file_tools as ft
import plot.plot as pt

import statistic.statistic_tools as st

running_modes = [0] * 100
running_modes[0] = 'plot all coauthor gap_year'
file_address_container = fac.FileAddressContainer()

index = 0
print(running_modes[index])
if index == 0:
    all_gap_year = ft.load_data_to_file('dict all coauthor citation gap year')
    citation_count,coauthor_count = st.count_frequency()
    all_gap_year[0] = 1
    st.div_sum_container(all_gap_year, 0, citation_count, coauthor_count)
    x, y = st.get_xy_from_container(all_gap_year)
    y = st.log_10_array(y)
    folder = file_address_container.get_file_addresses(sdp.source_folder, 'plot')
    pt.plot_figure(pl.plot, x, y, 'all coauthor citation gap year', folder, 'gap year', 'percent(log10)')
