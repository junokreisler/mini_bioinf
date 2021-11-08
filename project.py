from matplotlib import pyplot as plt
import pandas as pd
import functions as f
import seaborn as sb

##############################################################################
# GENERAL INFORMATION:
# This program was written on a Windows 11 laptop using Python 3.8.
# Make sure you have installed seaborn.

################################# PART 1 #####################################
# (1) import the relevant data and explore its details
# (2) create a dataframe to unite the 3 transcriptome datasets in one variable
# (3) Genes (exons/transcripts) obtained from Noemie Allet's genes.csv
##############################################################################

column_names = ['Gene', 'Expression']
DATA_1 = pd.read_csv('HATX3_counts', sep='\t')
DATA_2 = pd.read_csv('HATX8_counts', sep='\t')
DATA_3 = pd.read_csv('HATX12_counts', sep='\t')

DATA_1.columns = column_names
DATA_2.columns = column_names
DATA_3.columns = column_names

genes_length = pd.read_csv('genes.csv', sep=',', header = None)
column_names = ['Transcript','Length']
genes_length.columns = column_names

for i in range(0,len(DATA_1)): ### testing whether all gene names are in the same order
    if DATA_1.loc[i,'Gene'] != DATA_2.loc[i,'Gene']:
        print('doesn\'t match at', i, '!!!')
        break
    if i == 24424:
        print('all gene names are the same \nyou\'re good to go')

# joining the 3 separate datasets into one raw-read dataset
column_names = ['Gene','HATX3_counts','HATX8_counts','HATX12_counts']
DATA_ALL = pd.concat([DATA_1,DATA_2.Expression, DATA_3.Expression], axis = 1)
DATA_ALL.columns = column_names

DATA_Trimmed, missing_genes = f.trim_all_zeros(DATA_ALL) # genes with absent reads removed
print(len(missing_genes), 'genes removed from the dataset')

################################# PART 2 #####################################
# (1) pre-analysis of nonzero data
# (2) interim results and overall trends / facts
# (3) preparing data for further analysis

### PLOT DISTRIBUTION OF READ COUNTS
### VARIANCE OF GENE EXPRESSION PER GENE - MORE IN HIGHER OR LOWER EXPRESSION?
### FUNCTIONAL ASSOCIATION BETWEEN CLUSTERS AND THEIR CONTENTS
### RATIONALIZE NORMALIZATION, SCALING OF READ COUNTS DEPENDING ON SCALING
##############################################################################
# (1) plotting the raw data
manager = plt.get_current_fig_manager() # to obtain fullscreen images
manager.resize(*manager.window.maxsize())
# expression values were transformed in to their square roots to decrease the
# spread of values. log2 and log10 were tried but yielded too many similarly
# placed points, while sqrt transform gave plenty of clear outliers within a
# range of 0-750, diminishing it from 1

# checking reads before normalizing them
f.plot_comparative(DATA_Trimmed[0:-5], prefix = 'raw_trimmed')
hits_12, hits_23, hits_13 = f.miniclust3(DATA_Trimmed) # obtaining the list and locations of genes that are expressed most
                                                           # similarly between the 3 datasets
# normalizing...
DATA_Normalized = f.normalize(DATA_Trimmed, genes_length) # taxes approx. 2 minutes

# checking reads after normalizing them
f.plot_comparative(DATA_Normalized, prefix = 'normalized')
hits_12, hits_23, hits_13 = f.miniclust3(DATA_Normalized)
DATA_Normalized.loc[DATA_Normalized.index == 18935] # zoom in on any of the obtained plots with their y position,
                                                    # and you can see the gene/exon that corresponds

sim_hits = [len(hits_12), len(hits_23), len(hits_13)] # similarity comparisons

# sorting, obtaining cumulative data and checking read count distributions
HATX3_Cumulative = f.read_count_dist(pd.concat([DATA_Normalized.Gene, DATA_Normalized.HATX3_counts], axis = 1), sorted = False)
HATX8_Cumulative = f.read_count_dist(pd.concat([DATA_Normalized.Gene, DATA_Normalized.HATX8_counts], axis = 1), sorted = False)
HATX12_Cumulative = f.read_count_dist(pd.concat([DATA_Normalized.Gene, DATA_Normalized.HATX12_counts], axis = 1), sorted = False)

""" COMMENT ABOUT SORTING
The three datasets were separated for the sake of sorting. As there are still differences in the extent of 
gene expression between the three datasets, it's best to obtain a ranking for each dataset separately.
Then, when joining back based on gene names, we will be able to highlight any case where a gene in one dataset
is greatly over- or underexpressed compared to the rest.
Also, independent sorting + trimming shows the variance in read counts.
"""

cutoff = 10000

HATX3_C_Trimmed = f.trim_low_counts(HATX3_Cumulative, cutoff)
HATX8_C_Trimmed = f.trim_low_counts(HATX8_Cumulative, cutoff)
HATX12_C_Trimmed = f.trim_low_counts(HATX12_Cumulative, cutoff)

print(len(HATX3_C_Trimmed), len(HATX8_C_Trimmed), len(HATX12_C_Trimmed))

HATX8_C_Trimmed = HATX8_C_Trimmed[0:len(HATX3_C_Trimmed)]
HATX12_C_Trimmed = HATX12_C_Trimmed[0:len(HATX3_C_Trimmed)]

temp = pd.merge(HATX3_C_Trimmed,HATX8_C_Trimmed, on=HATX3_C_Trimmed.columns[0])
Trimmed_All = pd.merge(temp, HATX12_C_Trimmed, on=temp.columns[0])
Gene_Indices = Trimmed_All[Trimmed_All.columns[0]]
Trimmed_Values = Trimmed_All.drop(Trimmed_All.columns[0], axis = 1)
Trimmed_Values = Trimmed_Values.drop([Trimmed_Values.columns[1], Trimmed_Values.columns[3], Trimmed_Values.columns[5]], axis = 1)
''' CONCLUSIONS FROM PRE-ANALYSIS
1) The normalized expression rate seems to be very similar in all 3 datasets
2) There is a cluster of genes with nearby indexes that seem to be expressed much more prominently.
3) Plotting each dataset against one another yields two kinds of correlation graphs, overall suggesting
that sample 3 differs most from the rest.
4) "Mini-clustering" confirms this. The most similar are HATX3 and HATX8, with twice the number of closest matches
inbetween them than inbetween any of them and HATX12.
'''

################################# PART 3 #####################################
# (1) clustering and other more sophisticated processes
# (2) obtaining raw data / sorting for further analysis
# (3) defining parameters for data visualization
##############################################################################
sb.color_palette('mako') # changing the color_palette
startpos = 0
endpos = 100
Victory = sb.clustermap(Trimmed_Values[startpos:endpos])
clustered = Victory.dendrogram_row.reordered_ind # obtain the indices of the genes after reordering
Genes_Clustered_O = []
Clustered_Indices = []
for i in clustered:
    Clustered_Indices.append(i + startpos)
    Genes_Clustered_O.append([Clustered_Indices[-1], Gene_Indices[Clustered_Indices[-1]]]) ### contains genes and their indices in the order

Genes_Clustered_Order = [Gene_Indices[Clustered_Indices]]

print('Analysis has been successfully completed. Thank you for your time.')

"""
SAVING DATA FOR LATER ANALYSIS...........................................................
"""
unique_id = 'ribo_less'
with open('heatmap_results_'+ unique_id, '.txt', 'w') as f:
    for row in Genes_Clustered_O:
        f.write((str(row[0])))
        f.write(', ')
        f.write((row[1]))
        f.write('\n')

ribosomals = 0
for row in Genes_Clustered_O:
    if row[1][0:2] == 'Rp':
        ribosomals += 1
print('Among the captured genes,',ribosomals,'are ribosome-associated.')






"""
PROS: 
- The outputs are very interactive, at least while they are shown as figures when running the code.
This allows us to zoom into specific regions of interest and eventually find specific exons/genes that correspond
to a specific datapoint.
- The trimmed data, when not ambiguous, contains information about the non-expressed genes, which is also
necessary to see which genes are (most likely) inactive in the researched tissue/cell sample. 
The trimmed zero-value data only contains genes that are not expressed in ALL samples and is
stored in a separate variable.
- The heatmap can be easily adjusted to zoom into specific parts of the dataset in order to see how each
row of RPKM is clustered. Depending on the boundaries, clustering may change as well, which would highlight
differences in selected regions of the combined dataset.

CONS:
- The user must know what they are looking for in order to obtain useful information.
- There's a lot of repetitive code, a lot of it is used purely for the sake of comparing data during its transformation.
Half of the visualization (raw reads) does not contain any actually representative data.
- I didn't research a lot of specifics to create a unique representation of my data, and most of the time spend on the 
code was just to make it presentable and comparable.
- The cutoff value doesn't really mean anything if the cluster-heatmap doesn't plot all of the data.

ALSO: There was no tissue-specific hypothesis formulated when writing the data, which is both good and bad because
(+) I didn't subconsciously try to adjust the data to represent a specific idea
(+) The user can test their hypotheses interactively with plots, heatmaps
(-) There is a lot of potentially unhelpful data in the plots
(-) The data that is to be plotted also contains a lot of potentially meaningless data, and
meaningful data could be accidentally overlooked when not looking in the right location.
"""
