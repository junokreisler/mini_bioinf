########### sequences

a = 4382
b = 9069
sum = 0
for i in range(a,b+1):
    if i % 2 == 1:
        print(i, 'is odd?')
        sum += i
print(sum)

########### working with files

with open('rosalind_ini5.txt', 'r') as f:
    i = 1
    for line in f:
        if i % 2 == 0:
            print(line)
        i += 1

########## dictionaries

dict = {}
with open('rosalind_ini6.txt', 'r') as f:
    s = f.read()

words = ['']
count = 0
for i in s:
    words[count] += i
    if i == ' ' or i == '\n':
        words[count] = words[count][0:-1]
        words.append('')
        count += 1

for word in words:
    if word in dict:
        dict[word] += 1
    else:
        dict[word] = 1

for key in dict:
    print(key, dict[key])

