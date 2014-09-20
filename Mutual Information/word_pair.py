#!/usr/bin/python
from itertools import combinations
from math import log

'''
This method reads the txt file, get the total number of documents,
the vocabulary of collection, the list containing all documents,
and initialize the following dictionaries
1) the dictionary that stores the word and the number of documents 
   that contains it (N_A)
2) the dictionary that stores the word and the probability of documents
   that contains it (N_A+0.5/(1+N))
'''
def read_file(input_flie):
    N = 0 # Total number of documents
    vocabulary = set()
    documents = []
    word_frequency = {}
    for line in input_flie:
        each_line = line.rstrip().split(" ")
        documents.append(each_line)
        N += 1
        vocabulary |= set(each_line)
        for each_word in set(each_line):
            try:
                # Value is the number of documents containing 
                # the word
                word_frequency[each_word] += 1
            except KeyError:
                word_frequency[each_word] = 1
    vocabulary_list = list(vocabulary)
    # Smoothing the count
    word_probability = dict( (key, (word_frequency[key]+0.5)/(1+N)) \
                        for key in word_frequency )
    # print N # 3185
    # print len(vocabulary) # 1845
    return { 'total_documents': N,
             'documents': documents,
             'vocabulary': vocabulary_list,
             'word_frequency': word_frequency,
             'word_probability': word_probability
            }

'''
This method takes the document list as the input,
prints the top 10 word pairs with the largest count
and returns the word pair dictionary.
'''
def word_pair_frequency(documents):
    word_pair_dict = {}
    
    for each_document in documents:
        no_repetition = list(set(each_document))
        for each_pair in combinations(no_repetition, 2):
            # Sort each pair alphabetically within the tuple as key
            # Only store those pairs existed in the collection
            each_pair = tuple(sorted(each_pair))
            try:
                word_pair_dict[each_pair] += 1
            except KeyError:
                word_pair_dict[each_pair] = 1

    # Top 10 results
    sorted_dict = sorted( word_pair_dict.iteritems(), 
                          key=lambda x:x[1], 
                          reverse=True )
    # print len(sorted_dict) # 482492
    for i in range(0, 10):
        print str(sorted_dict[i][0]) + ": " + \
              str(sorted_dict[i][1])
    # It's not sorted now
    word_pair_dict = dict(sorted_dict)
    return word_pair_dict

'''
This method is a helper function for mutual information
calculation to get the joint probability.
'''
def joint(a, b, na, nb, nab, N):
    if a == 0 and b == 1:
        return (nb - nab + 0.25) / (1 + N)
    elif a == 1 and b == 0:
        return (na - nab + 0.25) / (1 + N)
    elif a == 1 and b == 1:
        return (nab + 0.25) / (1 + N)
    else:
        return (N - na - nb + nab + 0.25) / (1 + N)

'''
This method calculates the mutual information for two words.
It takes four inputs, prints the top 10 word pairs with 
the highest mutual information and returns the sorted list
of word pair list.
'''
def mutual_info(N, word_frequency, word_pair_dict, word_probability):
    mutual_info_dict = {}
    # Go over all possible pairs in the collection
    for each_pair in word_pair_dict:
        na = word_frequency[each_pair[0]]
        nb = word_frequency[each_pair[1]]
        nab = word_pair_dict[each_pair]
        pa = word_probability[each_pair[0]]
        pb = word_probability[each_pair[1]]
        a0b0 = joint(0, 0, na, nb, nab, N) * \
                log( joint(0, 0, na, nb, nab, N) / ((1 - pa) * (1 - pb)), 2 )
        a0b1 = joint(0, 1, na, nb, nab, N) * \
                log( joint(0, 1, na, nb, nab, N) / ((1 - pa) * pb), 2 )
        a1b0 = joint(1, 0, na, nb, nab, N) * \
                log( joint(1, 0, na, nb, nab, N) / (pa * (1 - pb)), 2 )
        a1b1 = joint(1, 1, na, nb, nab, N) * \
                log( joint(1, 1, na, nb, nab, N) / (pa * pb), 2 )
        result = a0b0 + a0b1 + a1b0 + a1b1
        mutual_info_dict[each_pair] = result

    # Top 10 results
    sorted_dict = sorted( mutual_info_dict.iteritems(), 
                          key=lambda x:x[1], 
                          reverse=True )
    # print len(sorted_dict) # 482492
    for i in range(0, 10):
        print str(sorted_dict[i][0]) + ": " + \
              str(sorted_dict[i][1])

    # It is a sorted list.
    mutual_info_list = sorted_dict
    return mutual_info_list

'''
This method finds the top n words that have the highest
mutual information with the input word.
'''
def find_relation(mutual_info_list, input_word, n):
    # (('input', 'output'), 0.06510989205016934)
    word_list = []
    for each_pair in mutual_info_list:
        if input_word in each_pair[0]:
            index = each_pair[0].index(input_word)
            other_index = 1^index
            word_list.append(each_pair[0][other_index])
    try:
        for i in range(0, n):
            print word_list[i]
    except IndexError:
        print "Invalid input_word or n!"

'''
This is the main function.
'''
if __name__ == '__main__':
    INPUT_FILE_NAME = "cacm.txt"
    input_flie = open(INPUT_FILE_NAME, 'r')
    result = read_file(input_flie)
    documents = result['documents']
    word_pair_dict = word_pair_frequency(documents)
    N = result['total_documents']
    word_frequency = result['word_frequency']
    word_probability = result['word_probability']
    print "---------------------------------"
    # The list preserves the sorted order
    mutual_info_list = mutual_info(N, word_frequency, 
                        word_pair_dict, word_probability)
    print "---------------------------------"
    find_relation(mutual_info_list, "programming", 5)






