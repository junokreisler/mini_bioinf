import random

tRNA = {'A': ['GCA','GCC','GCG','GCU'], 'B': ['GAU','GAC','AAU','AAC'], 'C': ['UGU','UGC'], 'D': ['GAU','GAC'],
          'E': ['GAA','GAG'], 'F': ['UUU','UUC'], 'G': ['GGA','GGU','GGC','GGG'], 'H': ['CAC','CAU'],
          'I': ['AUA','AUU','AUC'], 'J': ['UUA','UUG','CUA','CUU','CUG','CUC','AUA','AUU','AUC'],
          'K': ['AAA','AAG'], 'L': ['UUA','UUG','CUA','CUU','CUG','CUC'], 'M': 'AUG', 'N': ['AAU','AAC'], 'O': 'UAG',
          'P': ['CCA','CCU','CCG','CCC'], 'Q': ['CAA','CAG'], 'R': ['AGA','AGG','CGA','CGG','CGU','CGC'],
          'S': ['AGC','AGU','UCA','UCU','UCG','UCC'], 'T': ['ACA','ACC','ACU','ACG'], 'U': 'UGA',
          'V': ['GUA','GUC','GUU','GUG'], 'W': 'UGG', 'X': 0, 'Y': ['UAU','UAC'],
          'Z': ['GAA','GAG','CAA','CAG'], 'Start': 'AUG', 'Stop': ['UAA','UAG','UAA'], '.': ['UAA','UAG','UAA']}

sentence = 'Translate this sentence into 1 RNA sequence.'

def translator(AA): #AA (amino acid) is one character to be translated.
    try:
        AA = AA.upper()
    except:
        print('The character could not be found in the codon dictionary:', AA)
    if AA in tRNA:
        if isinstance(tRNA[AA],(int)):
            return ''.join(random.choice(['A','U','C','G']) for i in range(3))
        if isinstance(tRNA[AA],(str)):
            return tRNA[AA]
        else: # if it's a list
            return random.choice(tRNA[AA])
    else:
        return AA

def translate(sentence):
    translated = ''
    for i in sentence:
        if i == ' ':
            pass
        else:
            translated += translator(i)
    return translated

test = 'The quick brown fox jumps over the lazy dog. \n1 2 3 4 5 6 7 8 9 0 - = / \ , [ ] \' | ! @ # $ % ^ & * ( ) _ +'

decided = False
while not decided:
    decision = input('press enter to continue to writing your text, \n or write info/i/test/t for a demonstration...')
    if decision == 'info' or decision == 'i' or decision == 'test' or decision == 't':
        print('Example sentence: \n', test, '\n\nExample translated: \n', translate(test))
    elif decision == '':
        decided = True
        sentence = str(input('Write your text here: \n'))
        translated = translate(sentence)
        print('Translated to RNA: \n', translated)
        save = str(input('Press s to save the original and translated text to a text file.'))
        if save == 's' or save == 'S':
            with open('message_to_RNA.txt', 'w') as f:
                f.write(sentence + '\n')
                f.write(translated)
                print('Sentence and translation saved as message_to_RNA.txt')
        print('Thank you for using this tool!')
