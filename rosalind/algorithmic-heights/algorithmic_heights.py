# useful functions to avoid repetition

def fileLines(file): # transforms the given file into a list of strings = lines in their original order, \n removed
    with open(file) as f:
        raw = f.read()
        lines = ['']
        for i in raw:
            if i == '\n':
                lines.append('')
            else:
                lines[-1] += i
        lines.pop()
    return lines

def listPrint(list,txtname):
    with open(txtname + '.txt', 'w') as f:
        for i in range(0, len(list)):
            f.write(str(list[i]) + ' ')
    return print('File saved as ' + txtname + '.txt')

################# Fibonacci

def fibonacci(n):
    n_curr = 1
    n_prev = 0
    temp = 0
    for i in range(0,n-1): # as the first one is 0
        #print(n_curr)
        temp = n_curr
        n_curr += n_prev
        n_prev = temp
    return n_curr

fibonacci_n = 23
print(fibonacci(fibonacci_n))

################ Binary Search
# line 1 : num 1 /// line 2 : num 2 /// line 3 : set 1 /// line 4 : set 2
# num 1 is the size of the searchable array, num 2 is the number of searchable items
# line 3 is the given array, line 4 is the list of searchable items
# i don't know of any good purpose that num 2 could serve...
def bin_search(n1,array,find, moveup = 0):
    # n1 - first number of the file at first; later - length of array in an active iteration
    # array - the array which will be browsed through
    # find - the number that will be searched in the array
    mid_ind = n1 // 2

    if n1 == 1:
        if array[0] != find:
            return -1
    if find >= array[mid_ind]:
        if find == array[mid_ind]:
            return mid_ind+moveup
        else: # n1-mid_ind-1
            return bin_search(len(array[mid_ind:len(array)]), array[mid_ind:len(array)],find, moveup = moveup + mid_ind)
    if find < array[mid_ind]: # n1-mid_ind
        return bin_search(len(array[0:mid_ind]), array[0:mid_ind],find, moveup = moveup)

def do_theThing(res_array,n1,array,to_find):
    for i in to_find:
        res_array.append(bin_search(n1,array,i))
        if res_array[-1] != -1:
            res_array[-1] += 1
    return res_array

nums = fileLines('rosalind_bins.txt')

nums[0], nums[1] = int(nums[0]), int(nums[1])
sets = [[''],['']]
for n in range(2,4):
    for i in nums[n]:
        if i == ' ':
            sets[n-2][-1] = int(sets[n-2][-1])
            sets[n-2].append('')
        else:
            sets[n-2][-1] += i
    sets[n-2][-1] = int(sets[n-2][-1])

res = []
res = do_theThing(res,nums[0],sets[0],sets[1])

listPrint(res,'r_bins_res')

####################### Majority element - a O(n) = n version

def make_dict(array):
    occurences = {}
    for j in range(0,len(array)):
        i = array[j]
        if str(i) not in occurences:
            occurences[str(i)] = 1
        else:
            occurences[str(i)] += 1
    return occurences

def line_to_listofnums(line):
    list = ['']
    for i in line:
        if i == ' ':
            list[-1] = int(list[-1])
            list.append('')
        else:
            list[-1] += i
    list[-1] = int(list[-1])
    return list

lines = fileLines('rosalind_maj.txt')

lines_relevant = lines[1:len(lines)]
results = []

for i in range(0,len(lines_relevant)):
    new_list = line_to_listofnums(lines_relevant[i])
    print(new_list)
    dict = make_dict(new_list)
    values = list(dict.values())
    keys = list(dict.keys())

    print(max(values))
    if max(values) > len(new_list) // 2:
        yes = values.index(max(values))
        results.append(int(keys[yes]))
    else:
        results.append(-1)

listPrint(results,'r_maj_res')

######################## Degree Array

lines = fileLines('rosalind_deg.txt')

nums = line_to_listofnums(lines[0]) # first no. is the total number of nodes, second no. is the total number of links

res = [0 for i in range(0,nums[0])]

links = []
for i in range(1,len(lines)):
    links.append(line_to_listofnums(lines[i]))

for i in range(0,len(links)):
    for j in links[i]:
        res[j-1] += 1

listPrint(res,'r_deg_res')

######################## Insertion Sort
### let's just try to implement the presented algorithm in the task

lines = fileLines('rosalind_ins.txt')
array = line_to_listofnums(lines[1])

def insertion_sort(array):
    swaps = 0
    for i in range(1, len(array)):
        k = i
        while k > 0 and array[k] < array[k-1]:
            array[k],array[k-1] = array[k-1],array[k]
            k -= 1
            swaps += 1
    return(swaps)

print(insertion_sort(array))