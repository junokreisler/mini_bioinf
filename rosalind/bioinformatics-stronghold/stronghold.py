### Juno Kreisler's Rosalind attempts - Bioinformatics Stronghold
### run each part separately in the console to obtain individual task results
def dash():
    return print('------------------------------------------------------------------------------------')
################################ counting nucleotides
with open('rosalind_dna.txt', 'r') as f:
    s = f.read()

n = [0,0,0,0] # A, C, G, T
for i in s:
    if i == 'A':
        n[0] += 1
    if i == 'C':
        n[1] += 1
    if i == 'G':
        n[2] += 1
    if i == 'T':
        n[3] += 1

dash()
print('Counting nucleotides...')
print(n[0], n[1], n[2], n[3])

############################### DNA to RNA

with open('rosalind_rna.txt') as f:
    s = f.read()

s_RNA = ''
for i in s:
    if i == 'T':
        s_RNA += 'U'
    else:
        s_RNA += i

dash()
print('DNA to RNA...')
print(s_RNA)

############################## DNA complement

with open('rosalind_revc.txt') as f:
    s = f.read()

cDNA = ''

for i in s:
    if i == 'A':
        cDNA = 'T' + cDNA
    if i == 'C':
        cDNA = 'G' + cDNA
    if i == 'G':
        cDNA = 'C' + cDNA
    if i == 'T':
        cDNA = 'A' + cDNA

dash()
print('DNA complement...')
print(cDNA)

############################# rabbits?

with open('') as f:
    s = f.read()

'''
5 months, 3 pairs per litter
1
4 | 1 rep
7 | 4 rep
12+7 | 1+4+7 rep
[n, n+(n0..n-1)*k,
'''

dash()
print('stronghold 4')
print()

############################# GC content comparison

strings = []
names = []
with open('rosalind_gc.txt') as f:
    for line in f:
        if line[0] == '>':
            strings.append('')
            names.append(line[1:-1])
        else:
            strings[-1] += line[0:-1]

GC_contents = []
for seq in range(0,len(strings)):
    GC_contents.append(0)
    for i in strings[seq]:
        if i == 'G' or i == 'C':
            GC_contents[seq] += 1
    GC_contents[-1] /= len(strings[seq])

dash()
print('Largest GC content...')
loc = GC_contents.index(max(GC_contents))
print(names[loc])
print(max(GC_contents))

############################### hamming distance

with open('rosalind_hamm.txt') as f:
    strings = f.read()

s1 = ''
for i in range(0,len(strings)):
    if strings[i] == '\n':
        j = i+1
        break
    s1 += strings[i]

s2 = strings[j:-1]
ham = 0
for i in range(0,len(s1)):
    if s1[i] != s2[i]:
        ham += 1

dash()
print('Hamming distance...')
print(ham)

############################## Mendel's first law

with open('rosalind_iprb.txt') as f:
    s = f.read()

pop = [''] #will contain AA/Aa/aa as strings, then as integers
for i in s:
    pop[-1] += i
    if i == ' ' or i == '\n':
        pop[-1] = int(pop[-1])
        pop.append('')

if len(pop) == 4:
    pop.pop()
else:
    pop[-1] = int(pop[-1])

poptot = pop[0] + pop[1] + pop[2]

alleles = [pop[0]+pop[1],pop[1]+pop[2]] # number of A, number of a
d_offspring = [1*(pop[0]/poptot)*(pop[1]/(poptot-1)),  # AA x Aa = 1
               1*(pop[0]/poptot)*pop[2]/(poptot-1),    # AA x aa = 1
              0.5*(pop[1]/poptot)*pop[2]/(poptot-1),   # Aa x aa = 0.5
               1*(pop[0]/poptot)*(pop[0]-1)/(poptot-1),    # AA x AA = 1
               0.75*(pop[1]/poptot)*(pop[1]-1)/(poptot-1), # Aa x Aa = 0.75
               0]                                      # aa x aa = 0
d_sum = 0
for i in d_offspring:
    d_sum += i

d_percent = alleles[0]/(alleles[0]+alleles[1])

dash()
print('Mendel\'s First Law...')
print(d_percent)

############################ RNA to Protein

with open('') as f:
    s = f.read()
    if s[-1] == '\n':
        s = s[0:-1]

"""
to be continued .......... working on algorithmic heights this week.
"""