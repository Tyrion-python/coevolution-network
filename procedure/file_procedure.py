__author__ = 'Tyrion'

import data_operator.data_loader as dl
import data_operator.data_saver as ds
import data_operator.file_address_container as fac
import data_operator.file_tools as ft
import data_operator.original_data_formatter as odf
import data_operator.index_formatter as ifs

running_modes = [0] * 100

running_modes[0] = 'format original data'
running_modes[1] = 'cut file by end year'
running_modes[2] = 'cut file by paper tag'
running_modes[3] = 'write coauthor file'
running_modes[4] = 'format index'
index = 4
print(running_modes[index])

file_address_container = fac.FileAddressContainer()
if index == 0:
    scholar_file_addresses = file_address_container.get_file_addresses('real_2016')
    data_saver = ds.DataSaver(scholar_file_addresses)
    data_saver.open_all_file('w')
    original_data_formatter = odf.OriginalDataFormatter(data_saver)
    original_data_formatter.format_paper_year_file()
    original_data_formatter.format_paper_author_file()
    data_saver.close_all_files()
if index == 1:
    end_year = 1970
    scholar_file_addresses = file_address_container.get_file_addresses('real_2012_final')
    scholar_file_addresses_new = file_address_container.get_file_addresses('model')
    ft.cut_file_by_end_year(scholar_file_addresses['paper_year'], scholar_file_addresses_new['paper_year'], 1, end_year)
    ft.cut_file_by_end_year(scholar_file_addresses['paper_author'], scholar_file_addresses_new['paper_author'], 2,
                            end_year)
    ft.cut_file_by_end_year(scholar_file_addresses['paper_citation'], scholar_file_addresses_new['paper_citation'], 2,
                            end_year)
    ft.cut_file_by_end_year(scholar_file_addresses['coauthor'], scholar_file_addresses_new['coauthor'], 2,
                            end_year)
    ft.copy_file(scholar_file_addresses['max_index'], scholar_file_addresses_new['max_index'])
if index == 2:
    tags = ft.load_data_to_file('invalid_papers_set.txt')
    scholar_file_addresses = file_address_container.get_file_addresses('real_2012')
    scholar_file_addresses_new = file_address_container.get_file_addresses('real_2012_final')
    ft.cut_file_by_tag(tags, scholar_file_addresses['paper_year'], scholar_file_addresses_new['paper_year'], [0])
    ft.cut_file_by_tag(tags, scholar_file_addresses['paper_author'], scholar_file_addresses_new['paper_author'], [0])
    ft.cut_file_by_tag(tags, scholar_file_addresses['paper_citation'], scholar_file_addresses_new['paper_citation'], [0,
                                                                                                                      1])
if index == 3:
    file_addresses = file_address_container.get_file_addresses('real_1960')
    data_loader = dl.DataLoader(file_addresses)
    ft.write_coauthor_file(data_loader.paper_authors, data_loader.paper_year, file_addresses['coauthor'])
if index == 4:
    scholar_file_addresses = file_address_container.get_file_addresses('real_1960')
    scholar_file_addresses_new = file_address_container.get_file_addresses('model')
    index_formatter = ifs.IndexFormatter(scholar_file_addresses, scholar_file_addresses_new, 1960)
    index_formatter.format()
