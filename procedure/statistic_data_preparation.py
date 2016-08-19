__author__ = 'Tyrion'

import data_operator.data_loader as dl
import data_operator.file_address_container as fac

running_modes = [0] * 100
running_modes[0] = 'statistic: filter valid papers'
running_modes[1] = 'statistic: counter plot citation in degree distribution'
running_modes[2] = 'statistic None: count plot coauthor degree distribution'
running_modes[3] = 'statistic None: count citation largest component'
running_modes[4] = 'statistic None: count coauthor largest component'
running_modes[5] = 'statistic None:count coauthor average clustering'
running_modes[6] = 'statistic None:count coauthor distance'
running_modes[7] = 'statistic :count all coauthor citation gap year'
running_modes[8] = 'statistic :count year paper number'
running_modes[9] = 'statistic :count author old or new'
running_modes[10] = 'statistic None: get coauthor edges '
running_modes[11] = 'statistic:count all coauthor gap year'

source_folder = 'model'
# source_folder = 'real_2012_use'

index = 11

print(running_modes[index])
file_address_container = fac.FileAddressContainer()
if 'statistic' in running_modes[index]:
    if 'None' in running_modes[index]:
        data_loader = dl.DataLoader(file_address_container.get_file_addresses(source_folder), tag=False)
    else:
        data_loader = dl.DataLoader(file_address_container.get_file_addresses(source_folder))

if index == 1:
    data_loader.set_paper_in_papers()
if index == 2:
    coauthor_graph = data_loader.load_graph_from_file('coauthor')
    print(len(coauthor_graph.edges()))
if index == 3:
    citation_graph = data_loader.load_graph_from_file('citation')
if index == 4:
    coauthor_graph = data_loader.load_graph_from_file('coauthor')
if index == 5:
    coauthor_graph = data_loader.load_graph_from_file('coauthor')
if index == 6:
    coauthor_graph = data_loader.load_graph_from_file('coauthor')
if index == 7:
    data_loader.set_author_cited_author_years()
    data_loader.set_author_coauthor_years()
if index == 10:
    coauthor_graph = data_loader.load_graph_from_file('coauthor')
if index == 11:
    data_loader.set_author_coauthor_years()
