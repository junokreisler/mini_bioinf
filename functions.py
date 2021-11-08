import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

def plot_comparative(data, prefix):
    f1 = plt.figure()
    d1 = f1.add_subplot(311)
    d1.set_title(data.columns[1], fontsize=11)
    d1.scatter(data.index, data.iloc[:, 1], s=1)
    d2 = f1.add_subplot(312)
    d2.set_title(data.columns[2], fontsize=11)
    d2.scatter(data.index, data.iloc[:, 2], s=1, color='red')
    d3 = f1.add_subplot(313)
    d3.set_title(data.columns[3], fontsize=11)
    d3.scatter(data.index, data.iloc[:, 3], s=1, color='green')
    plt.tight_layout()
    f1.savefig(prefix +'_reads_plot.png', bbox_inches='tight')

    f2 = plt.figure()
    d_all = f2.add_subplot(111)
    d_all.set_title('HATX3/8/12 Read counts superimposed on each other')
    d_all.scatter(data.iloc[:, 1], data.index, s=1)
    d_all.scatter(data.iloc[:, 2], data.index, s=1, color='red')
    d_all.scatter(data.iloc[:, 3], data.index, s=1, color='green')
    plt.xlabel('Raw read counts')
    plt.ylabel('Gene index no.')
    f2.savefig(prefix +'_reads_superimposed.png', bbox_inches='tight')

    d_all.legend(['HATX3', 'HATX8', 'HATX12'])
    f3 = plt.figure()
    corr12 = f3.add_subplot(311)
    corr12.set_title('3/8')
    corr12.scatter(data.iloc[:, 1], data.iloc[:, 2], s=1)
    corr23 = f3.add_subplot(312)
    corr23.set_title('8/12')
    corr23.scatter(data.iloc[:, 2], data.iloc[:, 3], s=1)
    corr13 = f3.add_subplot(313)
    corr13.set_title('3/12')
    corr13.scatter(data.iloc[:, 1], data.iloc[:, 3], s=1)
    f3.savefig(prefix +'_reads_correlations.png', bbox_inches='tight')
    plt.show()
    return 'Plots have been saved with the prefix', prefix, 'in the working directory.'

def trim_all_zeros(data):
    data_cleaning = data
    check_len = len(data)
    george_not_found = [] # list of genes that aren't found, will be filled up on the go
    # input = pandas dataframe, genes + 3 sample data.
    # output = pandas dataframe with all genes removed that comprise 0% in all 3 samples
    for i in range(0,len(data_cleaning)): # runs through all genes and calculates overall expression
        sum_check = data_cleaning.iloc[i,1] + data_cleaning.iloc[i,2] + data_cleaning.iloc[i,3]
        if sum_check == 0: #if all samples have 0 reads for that gene, the sum is 0
            data_cleaning = data_cleaning.drop(i)
            check_len = len(data_cleaning)
            print('Removing index', i)
            george_not_found.append(data.iloc[i,0])
        if i == check_len-1:
            gnf = pd.DataFrame(george_not_found, columns=['Removed Genes'])
            break
    return data_cleaning, gnf

def normalize(data_raw, genes_length): #input = pandas 4 column dataframe, pd-read csv file [transcript, length]
    # 1) cut out the last 5 rows
    data_cut = data_raw[0:-5]
    data_norm = data_cut
    # 2) normalize the data per column by RPKM
    # RPKM = 10^9 * (reads mapped to transcript / (total reads * transcript length))
    for i in range(0, len(data_norm)):
        g = data_norm.iloc[i,0]
        l = int(genes_length[genes_length['Transcript'] == g].Length)
        for j in range(1, 4):  # only the read columns
            #data_norm.iloc[:, j] /= data_norm.iloc[:, j].sum()
            data_norm.iloc[i,j] = data_norm.iloc[i,j]* 10e9 / (l*data_norm.iloc[:, j].sum())
    return data_norm

def read_count_dist(data, sorted = False): # input = 2 column dataset [genes, counts in sample]
    if sorted == False: #sorting in descending order of read counts
        data_sorted = data.sort_values(by=data.columns[1], axis=0, ascending=False, inplace=False, kind='quicksort',
                            na_position='last', ignore_index=True, key=None)
    else:
        data_sorted = data # required because otherwise the function always takes the original 'data' information
                           # in each call in the function
    # counting cumulative %
    cumul = [data_sorted.iloc[0,1]]
    for i in range(1,len(data_sorted)):
        cumul.append(data_sorted.iloc[i,1]+cumul[i-1])
    # appending cumul to the input dataset
    name = [data.columns[1] + '_Cumulative']
    cumul = pd.DataFrame(cumul, columns=name)
    data_cumul = pd.concat([data_sorted, cumul.iloc[:, 0]], axis=1)
    # plotting cumulative reads
    plt.plot(data_cumul.iloc[:, -1])
    plt.xlabel('No. of gene in descending order of read counts')
    plt.ylabel('% of total reads')
    prefix = data.columns[1]
    plt.savefig(prefix+'_cumulative_read_dist.png')
    print("Plot saved as",prefix+'_cumulative_read_dist.png')
    return data_cumul

def trim_low_counts(data, cutoff = 50):
    data_trimmed = data[data.iloc[:,1] > cutoff]
    return data_trimmed

def miniclust3(data_input):
    ### INPUTS = 4-column dataframe, 1st column = genes, 2nd-4th column = read counts (values)
    ### at best, the data needs to be trimmed (trim_all_zeros)
    len_data = len(data_input)
    gene_name = data_input.columns[0]
    genes = data_input[gene_name] # for later extraction of gene names
    data = data_input.drop(gene_name, 1) # removing non-numeric values for analysis
    hits_12 = [] # will be filled with names of genes expressed most similarly in HATX3/HATX8
    hits_23 = [] # -//- HATX8/HATX12
    hits_13 = [] # -//- HATX3/HATX12
    for i in range(0,len_data):
        if abs(data.iloc[i, 0] - data.iloc[i,1]) < abs(data.iloc[i, 1] - data.iloc[i, 2]):  # if 1-2 > 1-3
            if abs(data.iloc[i,1] - data.iloc[i,2]) < abs(data.iloc[i,0]-data.iloc[i,1]):  # if 2-3 < 1-2
                hits_23.append(genes.iloc[i])
            else:
                hits_12.append(genes.iloc[i])
            if abs(data.iloc[i,1] - data.iloc[i,2]) > abs(data.iloc[i,0] - data.iloc[i,2]):  # if 2-3 > 1-3
                hits_13.append(genes.iloc[i])
            if abs(data.iloc[i,1] - data.iloc[i,2]) < abs(data.iloc[i,0] - data.iloc[i, 2]):
                hits_23.append(genes.iloc[i])
            else:
                continue
    sim_hits = [len(hits_12), len(hits_23), len(hits_13)]
    if sim_hits.index(max(sim_hits)) == 0:
        answer = 'The most similar read count sets are No.1 and No.2'
    if sim_hits.index(max(sim_hits)) == 1:
        answer = 'The most similar read count sets are No.2 and No.3'
    if sim_hits.index(max(sim_hits)) == 2:
        answer = 'The most similar read count sets are No.1 and No.3'
    print(sim_hits)
    print(answer)
    return hits_12, hits_23, hits_13

def ribosomal_search(data):
    ribosomals_positions = pd.DataFrame

    return ribosomals_positions